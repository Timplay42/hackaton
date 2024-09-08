from pydantic import BaseModel

class ToolsBase(BaseModel):
    type: str
    geo: str