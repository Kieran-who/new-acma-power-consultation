from pydantic import BaseModel
from typing import Optional, Union, List

class FilterItem(BaseModel):
    property: str
    value: Union[str, int, bool, List[str]]
    condition: str


class ContentRequest(BaseModel):
    path: str
    doc_id: str

class DocRetrieve(BaseModel):    
    search: Optional[str]
    filters: Optional[List[FilterItem]]
    excel: Optional[bool]