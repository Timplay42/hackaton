from fastapi import APIRouter, File, UploadFile
from .schema import Files
from .service import files_service

file_router = APIRouter()

@file_router.get('/')
async def get_safety(files=files_service):
    return await files.all()

@file_router.post('/clip/{file_id}', name='clip file')
async def create_clip(name: str, time_stamp: dict, file_id:str, files=files_service):
    return await files.create_clip(name, time_stamp ,file_id)

@file_router.post('/upload', name='upload file')
async def upload(file: UploadFile = File(...), files=files_service):
    return await files.upload(file)

@file_router.get('/all', name='get all files')
async def get_all(files=files_service):
    return await files.all()

@file_router.get('/file/{parent_file_id}')
async def get_file(parent_file_id: str, files=files_service):
    return await files.id(parent_file_id)