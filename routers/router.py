from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from models.models import ContentRequest, DocRetrieve, ChunkRetrieve, ChunkDel
from db.docs import DocumentManager
from db.chunks import ChunkManager
import os
from config import API_KEY, PASSWORD_COOKIE_NAME

router = APIRouter()

async def authenticate_request(request: Request):    
    if request.headers.get("X-Api-Key") == API_KEY:
        return
    if request.cookies.get(PASSWORD_COOKIE_NAME) == API_KEY:
        return
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
def get_file_path(doc_id, folder_path = './static/submissions'):    
    doc_id = doc_id.split('.')[0]    
    for file_name in os.listdir(folder_path):         
        if file_name.startswith(doc_id):
            return os.path.join(folder_path, file_name)

@router.get("/api/count")
async def get_meta(request: Request):
    await authenticate_request(request)
    dm = DocumentManager()
    return dm.get_docs_metadata()

@router.get("/api/pwcheck")
async def test_pw(request: Request):
    await authenticate_request(request)
    return 'success'

@router.get("/{doc_id:path}")
async def root(doc_id: str, request: Request):
    if doc_id:
            # Construct the full path to the file
            if doc_id.startswith('favicon'):
                return FileResponse('./static/favicon.ico')
            if doc_id.startswith('excel'):
                return FileResponse('./static/img/excel.png')
            await authenticate_request(request)
            file_location = get_file_path(doc_id)     
            if doc_id.startswith('academic') or doc_id.startswith('civil') or doc_id.startswith('political') or doc_id.startswith('government'):
                return FileResponse('./static/targetted_qs/aca.html')   
            if doc_id.startswith('platform') or doc_id.startswith('industry'):
                return FileResponse('./static/targetted_qs/digital.html') 
            if doc_id.startswith('news'):
                return FileResponse('./static/targetted_qs/news.html')              
            return FileResponse(file_location)
    else:        
        return FileResponse('./static/index.html')

@router.post("/api/docs")
async def get(doc_request: DocRetrieve, request: Request):
    await authenticate_request(request)
    dm = DocumentManager()
    search = doc_request.search
    filters = doc_request.filters
    excel_export = doc_request.excel
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
    
@router.post("/api/chunks")
async def get(chunk_request: ChunkRetrieve, request: Request):
    await authenticate_request(request)
    dm = ChunkManager()
    search = chunk_request.search
    filters = chunk_request.filters
    excel_export = chunk_request.excel
    search_weight = chunk_request.search_weight
    if excel_export:
        excel_file = dm.export_excel(filters, search)
        headers = {
            'Content-Disposition': 'attachment; filename="data.xlsx"'
        }
        return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
    if filters:
        return dm.search_chunks_filtered(filters, search, search_weight)
    if search and not filters:
        return dm.search_chunks(search, search_weight)
    else:
        return dm.get_all_chunks(limit=30000)
    
@router.delete("/api/chunks")
async def delete(chunk_request: ChunkRetrieve, request: Request):
    await authenticate_request(request)
    dm = ChunkManager()    
    return dm.delete_chunk(chunk_request.uuid)