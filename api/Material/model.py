import uuid

from sqlalchemy import ForeignKey
from utils.base.db_model_base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Materials(Base):
    __tablename__ = 'materials'

    name: Mapped[str]
    type: Mapped[str]


    
