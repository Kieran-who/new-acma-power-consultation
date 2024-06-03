from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse
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
            base_dir = Path("./static")
            # Construct the full path to the file
            file_location = base_dir / file_path
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