from sqlalchemy import ARRAY, Column, Integer, String, Text

from src.db.async_session_manager import Base
from pgvector.sqlalchemy import Vector


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(Text)
    company = Column(String)
    tags = Column(ARRAY(String))
    candidate_location = Column(String)
    job_type = Column(String)
    category = Column(String)
    salary = Column(String)
    remotive_id = Column(Integer, nullable=False, unique=True)
    embedding = Column(Vector(384))
