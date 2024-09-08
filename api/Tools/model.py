import uuid

from sqlalchemy import ForeignKey
from utils.base.db_model_base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Tools(Base):
    __tablename__ = 'tools'

    type: Mapped[str]
    geo: Mapped[str]

