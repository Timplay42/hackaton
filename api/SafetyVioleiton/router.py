from typing import List
from fastapi import APIRouter, UploadFile
from .schema import Safety
from .service import safety_service

safety_violetion_router = APIRouter()

@safety_violetion_router.get('/', response_model=List[Safety])
async def get_all_safety(safetys=safety_service):
    return await safetys.all()

@safety_violetion_router.get('/{sagety_id}', response_model=Safety)
async def get_all_safety(safety_id: str, safetys=safety_service):
    return await safetys.id(safety_id)

@safety_violetion_router.post('/')
async def get_safety(safety: Safety, safetys=safety_service):
    return await safetys.create(safety)
