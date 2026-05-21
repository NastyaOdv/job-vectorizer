from datetime import datetime

from sqlalchemy import Integer, Column, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from .schemas.tasks import TaskStatus
from src.db.async_session_manager import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    status = Column(Enum(TaskStatus), nullable=False)
    best_choice_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=True)
    result = Column(JSONB, nullable=True)
    cv_id = Column(Integer, ForeignKey("cv.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)