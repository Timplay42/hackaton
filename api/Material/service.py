from fastapi import Depends
from utils.base.database_session import AsyncDatabase
from utils.base.service import BaseRepository
from .model import Materials


class MaterialService(BaseRepository):
    model = Materials


async def get_material_service(session=Depends(AsyncDatabase.get_session)):
    return Materials(session)

material_service: MaterialService = Depends(get_material_service)

