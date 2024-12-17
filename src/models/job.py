from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: List[str] = Field(default_factory=list)
    salary_range: Optional[str] = None
    job_type: str  # Full-time, Part-time, Contract, etc.
    remote: bool = False
    url: Optional[str] = None
    source: str  # LinkedIn, Indeed, etc.

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: str
    posted_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class JobMatch(BaseModel):
    job: Job
    match_score: float
    match_reasons: List[str]

class JobSearch(BaseModel):
    keyword: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    remote: Optional[bool] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None

class JobResponse(Job):
    pass

class JobMatchResponse(JobMatch):
    pass
