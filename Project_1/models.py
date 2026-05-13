from tkinter import CASCADE

from sqlalchemy.sql import text
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, null
from sqlalchemy.orm import relationship

class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer , primary_key=True , nullable=False)
    title = Column(String , nullable=False)
    content = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)