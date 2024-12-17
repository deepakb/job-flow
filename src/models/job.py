from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class JobLocation(BaseModel):
    """
    Model representing a job location.
    
    Attributes:
        city: City name
        state: State or province name
        country: Country name
        is_remote: Whether remote work is allowed
        remote_type: Type of remote work (fully, hybrid, occasional)
    """
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State or province name")
    country: str = Field(..., description="Country name")
    is_remote: bool = Field(default=False, description="Whether remote work is allowed")
    remote_type: Optional[str] = Field(None, description="Type of remote work (fully, hybrid, occasional)")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "city": "San Francisco",
            "state": "California",
            "country": "United States",
            "is_remote": True,
            "remote_type": "hybrid"
        }
    })

class JobCompensation(BaseModel):
    """
    Model representing job compensation details.
    
    Attributes:
        salary_min: Minimum salary range
        salary_max: Maximum salary range
        currency: Currency code (e.g., USD)
        equity: Equity offering details (optional)
        benefits: List of benefits offered
    """
    salary_min: float = Field(..., description="Minimum salary range")
    salary_max: float = Field(..., description="Maximum salary range")
    currency: str = Field(..., description="Currency code (e.g., USD)")
    equity: Optional[str] = Field(None, description="Equity offering details")
    benefits: List[str] = Field(default_factory=list, description="List of benefits offered")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "salary_min": 100000,
            "salary_max": 150000,
            "currency": "USD",
            "equity": "0.1% - 0.5%",
            "benefits": [
                "Health insurance",
                "401(k) matching",
                "Unlimited PTO"
            ]
        }
    })

class JobBase(BaseModel):
    """
    Base model for job postings.
    
    Attributes:
        title: Job title
        company_name: Name of the hiring company
        company_url: Company website URL (optional)
        description: Detailed job description
        requirements: List of job requirements
        responsibilities: List of job responsibilities
        location: Job location details
        compensation: Compensation details
        job_type: Type of employment (full-time, part-time, contract)
        experience_level: Required experience level
        skills: Required skills
        nice_to_have: Optional skills that are beneficial
        posted_at: When the job was posted
        expires_at: When the job posting expires (optional)
        source: Source of the job posting (e.g., company website, job board)
        source_url: URL of the original job posting
    """
    title: str = Field(..., description="Job title")
    company_name: str = Field(..., description="Name of the hiring company")
    company_url: Optional[str] = Field(None, description="Company website URL")
    description: str = Field(..., description="Detailed job description")
    requirements: List[str] = Field(..., description="List of job requirements")
    responsibilities: List[str] = Field(..., description="List of job responsibilities")
    location: JobLocation = Field(..., description="Job location details")
    compensation: JobCompensation = Field(..., description="Compensation details")
    job_type: str = Field(..., description="Type of employment (full-time, part-time, contract)")
    experience_level: str = Field(..., description="Required experience level")
    skills: List[str] = Field(..., description="Required skills")
    nice_to_have: List[str] = Field(default_factory=list, description="Optional skills that are beneficial")
    posted_at: datetime = Field(..., description="When the job was posted")
    expires_at: Optional[datetime] = Field(None, description="When the job posting expires")
    source: str = Field(..., description="Source of the job posting")
    source_url: str = Field(..., description="URL of the original job posting")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "Senior Backend Engineer",
            "company_name": "Tech Corp",
            "company_url": "https://techcorp.com",
            "description": "We are seeking a talented Senior Backend Engineer...",
            "requirements": [
                "5+ years of Python experience",
                "Experience with FastAPI or similar frameworks",
                "Strong system design skills"
            ],
            "responsibilities": [
                "Design and implement scalable APIs",
                "Lead technical projects",
                "Mentor junior developers"
            ],
            "location": {
                "city": "San Francisco",
                "state": "California",
                "country": "United States",
                "is_remote": True,
                "remote_type": "hybrid"
            },
            "compensation": {
                "salary_min": 150000,
                "salary_max": 200000,
                "currency": "USD",
                "equity": "0.1% - 0.5%",
                "benefits": [
                    "Health insurance",
                    "401(k) matching",
                    "Unlimited PTO"
                ]
            },
            "job_type": "full-time",
            "experience_level": "senior",
            "skills": ["Python", "FastAPI", "AWS", "System Design"],
            "nice_to_have": ["Kubernetes", "GraphQL"],
            "posted_at": "2024-12-17T13:30:00Z",
            "source": "company_website",
            "source_url": "https://techcorp.com/careers/senior-backend-engineer"
        }
    })

class JobCreate(JobBase):
    """Model for creating a new job posting."""
    pass

class Job(JobBase):
    """
    Model representing a job posting.
    
    Attributes:
        id: Unique identifier for the job
        created_at: When the job was created
        updated_at: When the job was last updated
        is_active: Whether the job is active
    """
    id: str = Field(..., description="Unique identifier for the job")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the job was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="When the job was last updated")
    is_active: bool = Field(default=True, description="Whether the job is active")

class JobMatch(BaseModel):
    """
    Model representing a job match for a user.
    
    Attributes:
        job: The matched job posting
        match_score: Matching score between 0 and 1
        matching_skills: List of skills that match
        missing_skills: List of required skills that the user lacks
        experience_match: Whether the user's experience matches the requirements
    """
    job: Job = Field(..., description="The matched job posting")
    match_score: float = Field(..., ge=0, le=1, description="Matching score between 0 and 1")
    matching_skills: List[str] = Field(..., description="List of skills that match")
    missing_skills: List[str] = Field(..., description="List of required skills that the user lacks")
    experience_match: bool = Field(..., description="Whether the user's experience matches the requirements")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "job": {
                "id": "job123",
                "title": "Senior Backend Engineer",
                "company_name": "Tech Corp"
            },
            "match_score": 0.85,
            "matching_skills": ["Python", "FastAPI", "AWS"],
            "missing_skills": ["GraphQL"],
            "experience_match": True
        }
    })

class JobSearchParams(BaseModel):
    """
    Model for job search parameters.
    
    Attributes:
        keywords: Search keywords
        location: Desired location
        remote_only: Whether to show only remote jobs
        min_salary: Minimum salary requirement
        job_type: Desired job type
        experience_level: Desired experience level
        skills: Required skills to filter by
    """
    keywords: Optional[str] = Field(None, description="Search keywords")
    location: Optional[str] = Field(None, description="Desired location")
    remote_only: bool = Field(default=False, description="Whether to show only remote jobs")
    min_salary: Optional[float] = Field(None, description="Minimum salary requirement")
    job_type: Optional[str] = Field(None, description="Desired job type")
    experience_level: Optional[str] = Field(None, description="Desired experience level")
    skills: List[str] = Field(default_factory=list, description="Required skills to filter by")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "keywords": "backend engineer python",
            "location": "San Francisco",
            "remote_only": True,
            "min_salary": 120000,
            "job_type": "full-time",
            "experience_level": "senior",
            "skills": ["Python", "FastAPI"]
        }
    })

class JobResponse(Job, JobBase):
    """Model for a job response."""
    pass

class JobMatchResponse(JobMatch):
    """Model for a job match response."""
    pass
