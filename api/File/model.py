import json
from typing import List
import uuid
from utils.base.db_model_base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import LargeBinary, ForeignKey, JSON


class File(Base):
    __tablename__ = 'files'
    
    name: Mapped[str]
    original_path: Mapped[str] = mapped_column(nullable=True)
    mime_type: Mapped[str]
    time_stamp: Mapped[dict] = mapped_column(type_=JSON, default={})


    

class FileChildren(Base):
    __tablename__ = 'files_children'

    queue: Mapped[int]
    name: Mapped[str]
    original_path: Mapped[str]
    mime_type: Mapped[str]
    parent_file_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(column='files.id'), nullable=False)


    
