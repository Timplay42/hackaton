import uuid

from sqlalchemy import ForeignKey
from utils.base.db_model_base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Safety(Base):
    __tablename__ = 'safety'

    type: Mapped[str]
    description: Mapped[str]

