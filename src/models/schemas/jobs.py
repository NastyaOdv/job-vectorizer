from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    tags: Optional[List[str]] = None
    candidate_location: Optional[str] = None
    job_type: Optional[str] = None
    category: Optional[str] = None
    salary: Optional[str] = None
    remotive_id: int


class RemotiveJob(BaseModel):
    id: int
    title: str
    company_name: str
    category: str
    tags: List[str]
    job_type: Optional[str] = None
    candidate_required_location: Optional[str] = None
    salary: Optional[str] = None
    description: Optional[str] = None


    class Config:
        from_attributes = True