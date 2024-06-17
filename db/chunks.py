from .db_instance import DBClient
from models.models import FilterItem
from weaviate.classes.query import MetadataQuery
from pydantic import BaseModel
import weaviate.classes as wvc
import pandas as pd
from ai_client import get_vector
from io import BytesIO

class Chunk(BaseModel):
    group: str
    submission_uniqueId: str    
    chunk_text: str
    support: str
    regulation_type: str    
    regulator_trust: str    
    submitter: str
    chunk_index: int

class ChunkManager:
    def __init__(self):
        self.client = None
        self.chunks = None

    def init_client(self):
        if not self.client:
            self.client = DBClient()
            self.chunks = self.client.collections.get("Chunk")
            print('chunk client initialized')
    
    def update_chunk(self, id, data_obj: Chunk):
        self.init_client()                
        self.chunks.data.update(id, data_obj)        
        return
    
    def update_single_property(self, id, property_name, value):
        self.init_client()
        self.chunks.data.update(id, properties={property_name: value})
        return

    def search_chunks(self, query, search_weighting = 1):
        self.init_client()        
        query_vector = get_vector(query)
        if search_weighting == 1:                
            result = self.chunks.query.near_vector(
                near_vector=query_vector,
                limit=5000,                
                return_metadata=MetadataQuery(distance=True)
            )            
        else:
            result = (
                self.chunks.query.hybrid(
                    query=query,
                    query_properties=["chunk_text"],
                    vector=query_vector,
                    alpha=search_weighting,
                    limit=5000
                )            
            )
        chunks = []
        for obj in result.objects:            
            chunk = obj.properties
            chunk['uuid'] = obj.uuid
            chunk['distance'] = obj.metadata.distance if hasattr(obj.metadata, 'distance') else None 
            chunks.append(chunk)
        return chunks

    def search_chunks_filtered(self, filter_objects, search = None, search_weighting = 1):
        self.init_client()
        # Initialize the filter with None
        combined_filter = None

        # Iterate through the array and build the filter
        for filter_item in filter_objects:
            property_name = filter_item.property            
            value = filter_item.value
            condition = filter_item.condition 
            
            # Create the filter based on the condition
            if condition == "equal":
                current_filter = wvc.query.Filter.by_property(property_name).equal(value)
            elif condition == "less_than":
                current_filter = wvc.query.Filter.by_property(property_name).less_than(value)
            elif condition == 'contains_any':
                current_filter = wvc.query.Filter.by_property(property_name).contains_any(value)
            elif condition == 'not_equal':
                current_filter = wvc.query.Filter.by_property(property_name).not_equal(value)    
            
            # Combine the filter with the previous ones
            if combined_filter is None:
                combined_filter = current_filter
            else:
                combined_filter = combined_filter & current_filter         
                
        if search:
            query_vector = get_vector(search)
            if search_weighting == 1:                
                result = self.chunks.query.near_vector(
                    near_vector=query_vector,
                    limit=5000,
                    filters=combined_filter,
                    return_metadata=MetadataQuery(distance=True)
                )                
            else:                
                result = self.chunks.query.hybrid(
                    query=search,
                    query_properties=["chunk_text"],
                    vector=query_vector,
                    alpha=search_weighting,                
                    filters=combined_filter,
                    limit=5000
                )
        else:    
            result = self.chunks.query.fetch_objects(
                filters=combined_filter,
                limit=5000,
            )
        chunks = []        
        for obj in result.objects:            
            doc = obj.properties
            doc['distance'] = obj.metadata.distance if hasattr(obj.metadata, 'distance') else None 
            doc['uuid'] = obj.uuid            
            chunks.append(doc)
        return chunks 

    def get_all_chunks(self, limit=5000):
        self.init_client()        
        result = self.chunks.query.fetch_objects(
            limit=limit,
        )
        docs = []
        for obj in result.objects:
            doc = obj.properties
            doc['uuid'] = obj.uuid            
            docs.append(doc)
        return docs

    def get_chunks_metadata(self):
        self.init_client()
        result = self.chunks.aggregate.over_all(total_count=True),        
        return result

    def chunks_getter(self, id):
        self.init_client()
        doc = self.chunks.query.fetch_object_by_id(id)
        return doc

    def delete_chunk(self, id):
        self.init_client()        
        self.chunks.data.delete_by_id(id)
        return    

    def new_chunk(self, data_obj: Chunk, replace_existing = False):
        self.init_client()
        custom_vector = get_vector(data_obj["chunk_text"])
        url_existing = self.search_chunks_filtered([FilterItem(property='submission_uniqueId', value=data_obj["submission_uniqueId"], condition='equal'),FilterItem(property='chunk_index', value=data_obj["chunk_index"], condition='equal')])
        if len(url_existing) > 0:
            if replace_existing:
                print('deleting chunk, then adding new one')
                self.delete_chunk(url_existing[0]['uuid'])
            else:
                return               
        try:
            new_doc = self.chunks.data.insert(
                properties=data_obj,
                vector=custom_vector
            )
            return new_doc
        except Exception as e:
            print(e)
            return None    
        
    def export_excel(self, filter_objects, search=None):
        self.init_client()
        if filter_objects and len(filter_objects) > 0:
            docs = self.search_chunks_filtered(filter_objects, search)
        elif search:
            docs = self.search_chunks(search)
        else:
            docs = self.get_all_chunks()
        for doc in docs:
            del doc["uuid"]
        # Convert docs to a pandas DataFrame
        df = pd.DataFrame(docs)
        
        # Create a BytesIO buffer to hold the Excel file in memory
        output = BytesIO()
        # Export DataFrame to Excel and write to the in-memory buffer
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        # After exiting the with block, the Excel file is saved in the buffer.
        # Reset the buffer position to the start
        output.seek(0)
        
        # Return the in-memory buffer containing the Excel file
        return output


