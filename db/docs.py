from .db_instance import DBClient
from models.models import FilterItem
from pydantic import BaseModel
from typing import List, Optional, Dict
import weaviate.classes as wvc
import pandas as pd
from az_client import get_vector
from io import BytesIO
import json

class Document(BaseModel):
    author: str
    substantive_submission: str
    responder_category: str    
    support: str
    motivations: List[str]
    regulation: str
    perceived_impact: str
    regulator_trust: str
    file_name: str
    definitions: str
    questions: Optional[Dict]

class DocumentManager:
    def __init__(self):
        self.client = None
        self.docs = None

    def init_client(self):
        if not self.client:
            self.client = DBClient()
            self.docs = self.client.collections.get("Submission")
            print('client initialized')
    
    def update_doc(self, id, data_obj: Document):
        self.init_client()                
        self.docs.data.update(id, data_obj)        
        return

    def search_docs(self, query):
        self.init_client()        
        query_vector = get_vector(query)
        result = (
            self.docs.query.hybrid(
                query=query,
                query_properties=["author",  "responder_category", "support", "motivations", "regulation",  "perceived_impact", "regulator_trust", "file_name"],
                vector=query_vector,
                alpha=0.75,
                limit=2500
            )            
        )
        docs = []
        for obj in result.objects:            
            doc = obj.properties
            if 'questions' in doc:
                doc['questions'] = json.loads(doc['questions'])
            doc['uuid'] = obj.uuid
            docs.append(doc)
        return docs

    def search_docs_filtered(self, filter_objects, search = None):
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
            result = (self.docs.query.hybrid(
                query=search,
                query_properties=["author",  "responder_category", "support", "motivations", "regulation",  "perceived_impact", "regulator_trust", "file_name"],
                vector=query_vector,
                alpha=0.75,                
                filters=combined_filter,
                limit=2500
            ))
        else:    
            result = (self.docs.query.fetch_objects(
                filters=combined_filter,
                limit=2500
            ))
        docs = []
        for obj in result.objects:
            doc = obj.properties
            if 'questions' in doc:
                doc['questions'] = json.loads(doc['questions'])
            doc['uuid'] = obj.uuid
            docs.append(doc)
        return docs 

    def get_all_docs(self, limit=5000):
        self.init_client()        
        result = self.docs.query.fetch_objects(
            limit=limit,            
        )        
        docs = []
        for obj in result.objects:
            doc = obj.properties
            if 'questions' in doc:
                doc['questions'] = json.loads(doc['questions'])
            doc['uuid'] = obj.uuid
            docs.append(doc)
        return docs

    def get_docs_metadata(self):
        self.init_client()
        result = self.docs.aggregate.over_all(total_count=True),        
        return result

    def doc_getter(self, id):
        self.init_client()        
        doc = self.docs.query.fetch_object_by_id(id)
        return doc

    def delete_doc(self, id):
        self.init_client()
        self.docs.data.delete_by_id(id)
        return    

    def new_doc(self, data_obj: Document, custom_vector, replace_existing = False):
        self.init_client()
        url_existing = self.search_docs_filtered([FilterItem(property='file_name', value=data_obj["file_name"], condition='equal')])
        if len(url_existing) > 0:
            if replace_existing:
                print('delete doc, then add')
                self.delete_doc(url_existing[0]['uuid'])
            else:
                return               
        try:
            new_doc = self.docs.data.insert(
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
            docs = self.search_docs_filtered(filter_objects, search)
        elif search:
            docs = self.search_docs(search)
        else:
            docs = self.get_all_docs()
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


