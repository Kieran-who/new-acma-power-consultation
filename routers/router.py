from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse
from models.models import ContentRequest, DocRetrieve
from db.docs import DocumentManager
from pathlib import Path
import os

router = APIRouter()

@router.get("/api/count")
async def get_meta():
    dm = DocumentManager()
    return dm.get_docs_metadata()

def get_file_path(doc_id, folder_path = './static/submissions'):    
    doc_id = doc_id.split('.')[0]    
    for file_name in os.listdir(folder_path):         
        if file_name.startswith(doc_id):
            return os.path.join(folder_path, file_name)

@router.get("/{doc_id:path}")
async def root(doc_id: str):
    if doc_id:
            # Construct the full path to the file
            if doc_id.startswith('favicon'):
                return FileResponse('./static/favicon.ico')
            file_location = get_file_path(doc_id)            
            return FileResponse(f'{file_location}')
    else:
        return FileResponse('./static/index.html')

@router.post("/api/docs")
async def get(request: DocRetrieve):
    dm = DocumentManager()
    search = request.search
    filters = request.filters
    excel_export = request.excel
    if excel_export:
        excel_file = dm.export_excel(filters, search)
        headers = {
            'Content-Disposition': 'attachment; filename="data.xlsx"'
        }
        return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
    if filters:
        return dm.search_docs_filtered(filters, search)
    if search and not filters:
        return dm.search_docs(search)
    else:
        return dm.get_all_docs(limit=2500)

@router.post("/api/content")
async def content(request: ContentRequest):    
    dm = DocumentManager()
    nearby = dm.near_by(request.doc_id)
    with open(request.path, 'r') as file:
        return {"file": file.read(), "nearby": nearby}