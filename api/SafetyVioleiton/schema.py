from pydantic import BaseModel

class Safety(BaseModel):
    type: str
    descritpion: str
    