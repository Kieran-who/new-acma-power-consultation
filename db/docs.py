from .db_instance import DBClient
from pydantic import BaseModel
from typing import List
import weaviate.classes as wvc
from az_client import get_vector

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
                limit=100
            )            
        )
        docs = []
        for obj in result.objects:            
            doc = obj.properties
            if 'motivation' in doc:
                fixed_motivation = []
                motivations = doc["motivation"].split('. ')
                for motivation in motivations:
                    mot_split = motivation.strip().split('\n')
                    for mot in mot_split:                    
                        if len(mot) > 3:
                            fixed_motivation.append(mot)                
                doc['motivations'] = fixed_motivation
                doc.pop('motivation', None)
                self.update_doc(obj.uuid, doc)
            doc['uuid'] = obj.uuid
            docs.append(doc)
        return docs

    def search_docs_filtered(self, property: str, property_value):
        self.init_client()                
        result = (self.docs.query.fetch_objects(
            filters=wvc.query.Filter.by_property(property).equal(property_value),
            limit=1000
        ))
        docs = []
        for obj in result.objects:
            doc = obj.properties
            if 'motivation' in doc:
                fixed_motivation = []
                motivations = doc["motivation"].split('. ')
                for motivation in motivations:
                    mot_split = motivation.strip().split('\n')
                    for mot in mot_split:                    
                        if len(mot) > 3:
                            fixed_motivation.append(mot)                
                doc['motivations'] = fixed_motivation                
                self.update_doc(obj.uuid, doc)
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
            if 'motivation' in doc:
                fixed_motivation = []
                motivations = doc["motivation"].split('. ')
                for motivation in motivations:
                    mot_split = motivation.strip().split('\n')
                    for mot in mot_split:                    
                        if len(mot) > 3:
                            fixed_motivation.append(mot)                
                doc['motivations'] = fixed_motivation
                doc.pop('motivation', None)
                self.update_doc(obj.uuid, doc)
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
        url_existing = self.search_docs_filtered('file_name', data_obj["file_name"])
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