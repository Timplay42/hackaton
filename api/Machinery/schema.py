from pydantic import BaseModel
from typing import Optional, List



class MachineSafety(BaseModel):
    type: str
    status: str
    geo: str