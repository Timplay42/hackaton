from typing import List
from fastapi import APIRouter
from .schema import MaterialBase
from .service import material_service

material_router = APIRouter()

@material_router.get('/all', name='get all material', response_model=List[MaterialBase])
async def get_all_material(materials=material_service):
    return await materials.all()

@material_router.post('/create')
async def create(machinery : MaterialBase, materials=material_service):
    return await materials.create(machinery)

@material_router.post('/update')
async def update(machinery: MaterialBase, materials=material_service):
    return await materials.update(machinery)