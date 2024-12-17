"""
Models for resume-related functionality.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SkillAssessment(BaseModel):
    """Model for skill assessment results."""
    name: str
    category: str = Field(..., description="technical, soft, or domain")
    proficiency: int = Field(..., ge=1, le=5, description="Skill proficiency level (1-5)")
    years_experience: float
    context: str = Field(..., description="Where and how the skill was used")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance to target job")

class ResumeEnhancement(BaseModel):
    """Model for resume enhancement suggestions."""
    content_suggestions: Dict[str, List[str]] = Field(
        ...,
        description="Section-wise content improvement suggestions"
    )
    ats_score: Dict[str, Any] = Field(
        ...,
        description="ATS compatibility score and feedback"
    )
    skill_assessment: List[SkillAssessment] = Field(
        ...,
        description="Detailed assessment of skills"
    )
    industry_alignment: Optional[Dict[str, Any]] = Field(
        None,
        description="Industry-specific recommendations"
    )
    career_narrative: Optional[Dict[str, Any]] = Field(
        None,
        description="Career progression analysis"
    )

class ResumeCreate(BaseModel):
    """Model for resume creation."""
    file_name: str
    file_content: bytes
    target_job_title: Optional[str] = None
    target_industry: Optional[str] = None

class Resume(BaseModel):
    """Model for resume data."""
    id: str
    user_id: str
    file_name: str
    text: str
    structured_data: Dict[str, Any]
    skill_assessment: Optional[List[SkillAssessment]] = None
    ats_score: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResumeResponse(Resume):
    """
    Model for resume responses in API endpoints.
    Inherits all fields from the base Resume model.
    """
    pass
