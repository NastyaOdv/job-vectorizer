from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, Column, String, DateTime

from src.db.async_session_manager import Base


class CV(Base):
    __tablename__ = "cv"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    embedding = Column(Vector(384), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)