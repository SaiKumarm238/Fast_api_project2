from fastapi import APIRouter, File, UploadFile, HTTPException, status
import shutil
from fastapi.responses import FileResponse

router = APIRouter(
    prefix='/file',
    tags=["file"]
)

@router.post('/')
def get_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {"data":lines}

@router.post('/upload_file')
def upload_file(upload_file: UploadFile = File(...)):
    path = f"files/{upload_file.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {
        "uploades_in": path,
        "type" : upload_file.content_type
    }

@router.get('/download/{name}', response_class=FileResponse)
def download_file(name:str):
    path = f"files/{name}"
    # if not path:
    #     raise HTTPException(status_code=statu s.HTTP_404_NOT_FOUND, detail=f"File with the name {name} is not found")
    return path