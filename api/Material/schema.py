from pydantic import BaseModel

class MaterialBase(BaseModel):
    name: str
    type: str