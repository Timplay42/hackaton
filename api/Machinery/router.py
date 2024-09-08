from typing import List
from fastapi import APIRouter
from .schema import MachineSafety
from .service import machine_safety_service

machinery_router = APIRouter()

@machinery_router.get('/all', name='get all machine safety', response_model=List[MachineSafety])
async def get_safety(safetys=machine_safety_service):
    return await safetys.all()

@machinery_router.post('/create')
async def create_machinery(machinery : MachineSafety, machinerys=machine_safety_service):
    return await machinerys.create(machinery)

@machinery_router.post('/update')
async def update_machinery(machinery: MachineSafety, machinerys=machine_safety_service):
    return await machinerys.update(machinery)