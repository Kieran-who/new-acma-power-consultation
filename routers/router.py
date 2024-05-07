from fastapi import APIRouter
from fastapi.responses import FileResponse
from models.models import ContentRequest, DocRetrieve
from db.docs import DocumentManager
from pathlib import Path

router = APIRouter()

@router.get("/api/count")
async def get_meta():
    dm = DocumentManager()
    return dm.get_docs_metadata()

@router.get("/{file_path:path}")
async def root(file_path: str):
    if file_path:
            base_dir = Path("./static/submissions")
            # Construct the full path to the file
            file_location = base_dir / file_path
            return FileResponse(f'{file_location}')
    else:
        return FileResponse('./static/index.html')

@router.post("/api/docs")
async def get(request: DocRetrieve):    
    dm = DocumentManager()
    search = request.search
    if search:
        return dm.search_docs(search)
    else:
        return dm.get_all_docs(limit=100)
    

@router.post("/api/content")
async def content(request: ContentRequest):    
    dm = DocumentManager()
    nearby = dm.near_by(request.doc_id)
    with open(request.path, 'r') as file:
        return {"file": file.read(), "nearby": nearby}