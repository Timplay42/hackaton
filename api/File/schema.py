from pydantic import BaseModel
from typing import Optional, List



class Files(BaseModel):
    name: str
    original_path: str
    mime_type: str
    time_stamp: dict