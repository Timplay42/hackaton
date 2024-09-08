from typing import List
from fastapi import APIRouter, UploadFile
from .schema import ToolsBase
from .service import tool_service

tools_router = APIRouter()

@tools_router.get('/', response_model=List[ToolsBase])
async def get_all_tools(tools=tool_service):
    return await tools.all()

@tools_router.get('/{tool_id}', response_model=ToolsBase)
async def get_tools_id(safety_id: str, tools=tool_service):
    return await tools.id(safety_id)

@tools_router.post('/')
async def get_tools(tool: ToolsBase, tools=tool_service):
    return await tools.create(tool)

@tools_router.post('/update')
async def get_tools(tool: ToolsBase, tools=tool_service):
    return await tools.update(tool)