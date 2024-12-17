from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: datetime
    end_date: Optional[datetime] = None
    gpa: Optional[float] = None

class Experience(BaseModel):
    company: str
    title: str
    location: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: List[str]
    skills: List[str]

class Resume(BaseModel):
    id: str
    user_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ResumeCreate(BaseModel):
    file_content: bytes
    file_name: str

class ResumeEnhancement(BaseModel):
    summary_suggestions: List[str]
    skill_suggestions: List[str]
    experience_suggestions: List[str]
    education_suggestions: List[str]

class ResumeResponse(Resume):
    pass
