"""
Application models for the job application system.

This module defines the data models for job applications, including:
- Application status tracking
- Application metadata
- Interview scheduling
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class ApplicationStatus(str, Enum):
    """Status of a job application."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWING = "interviewing"
    OFFER_RECEIVED = "offer_received"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class ApplicationBase(BaseModel):
    """Base model for job applications."""
    job_id: str = Field(..., description="ID of the job being applied to")
    resume_id: str = Field(..., description="ID of the resume used for application")
    cover_letter: Optional[str] = Field(None, description="Optional cover letter text")
    status: ApplicationStatus = Field(
        default=ApplicationStatus.DRAFT,
        description="Current status of the application"
    )
    notes: Optional[str] = Field(None, description="Internal notes about the application")

class ApplicationCreate(ApplicationBase):
    """Model for creating a new job application."""
    pass

class ApplicationUpdate(BaseModel):
    """Model for updating an existing job application."""
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    cover_letter: Optional[str] = None

class JobApplication(ApplicationBase):
    """Complete job application model with metadata."""
    id: str = Field(..., description="Unique identifier for the application")
    user_id: str = Field(..., description="ID of the user who submitted the application")
    created_at: datetime = Field(..., description="When the application was created")
    updated_at: datetime = Field(..., description="When the application was last updated")
    submitted_at: Optional[datetime] = Field(
        None,
        description="When the application was submitted"
    )
    interview_date: Optional[datetime] = Field(
        None,
        description="Scheduled interview date and time"
    )

    class Config:
        """Pydantic model configuration."""
        from_attributes = True
