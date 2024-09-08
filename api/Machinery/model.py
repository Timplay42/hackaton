import uuid

from sqlalchemy import ForeignKey
from utils.base.db_model_base import Base
from sqlalchemy.orm import Mapped, mapped_column


class SafetyMachinery(Base):
    __tablename__ = 'safety_machinery'

    type: Mapped[str]
    status: Mapped[str]
    geo: Mapped[str]

    
