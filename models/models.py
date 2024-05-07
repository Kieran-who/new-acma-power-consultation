from pydantic import BaseModel
from typing import Optional

class ContentRequest(BaseModel):
    path: str
    doc_id: str    

class DocRetrieve(BaseModel):    
    search: Optional[str]