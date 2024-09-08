from .model import Tools
from fastapi import Depends, Form, HTTPException, status
from utils.base.database_session import AsyncDatabase
from utils.base.service import BaseRepository
from sqlalchemy import select

class ToolService(BaseRepository):
    model = Tools
    

async def get_tool_service(session=Depends(AsyncDatabase.get_session)):
    return ToolService(session)

tool_service: ToolService = Depends(get_tool_service)

