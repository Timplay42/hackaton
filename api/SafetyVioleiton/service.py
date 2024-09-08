from .model import Safety
from fastapi import Depends, Form, HTTPException, status
from utils.base.database_session import AsyncDatabase
from utils.base.service import BaseRepository
from sqlalchemy import select

class SafetyService(BaseRepository):
    model = Safety
    
    async def get_safety_by_type(self, type: str):
        safety = (await self.session.scalars(select(self.model).where(self.model.type == type))).first()
        return safety

async def get_safety_service(session=Depends(AsyncDatabase.get_session)):
    return SafetyService(session)

safety_service: SafetyService = Depends(get_safety_service)

