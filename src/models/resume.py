from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Education(BaseModel):
    """
    Model representing educational background.
    
    Attributes:
        institution: Name of the educational institution
        degree: Type of degree obtained
        field_of_study: Area of study or major
        start_date: When the education began
        end_date: When the education was completed (optional, for ongoing education)
        gpa: Grade Point Average (optional)
    """
    institution: str = Field(..., description="Name of the educational institution")
    degree: str = Field(..., description="Type of degree obtained")
    field_of_study: str = Field(..., description="Area of study or major")
    start_date: datetime = Field(..., description="Start date of education")
    end_date: Optional[datetime] = Field(None, description="End date of education (if completed)")
    gpa: Optional[float] = Field(None, description="Grade Point Average")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "institution": "Stanford University",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "start_date": "2018-09-01T00:00:00Z",
            "end_date": "2022-06-01T00:00:00Z",
            "gpa": 3.8
        }
    })

class Experience(BaseModel):
    """
    Model representing work experience.
    
    Attributes:
        company: Name of the employer
        title: Job title or position
        location: Work location
        start_date: When the position began
        end_date: When the position ended (optional, for current positions)
        description: List of responsibilities and achievements
        skills: Skills utilized in this position
    """
    company: str = Field(..., description="Name of the employer")
    title: str = Field(..., description="Job title or position")
    location: str = Field(..., description="Work location")
    start_date: datetime = Field(..., description="Start date of employment")
    end_date: Optional[datetime] = Field(None, description="End date of employment (if not current)")
    description: List[str] = Field(..., description="List of responsibilities and achievements")
    skills: List[str] = Field(..., description="Skills utilized in this position")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "company": "Tech Corp",
            "title": "Senior Software Engineer",
            "location": "San Francisco, CA",
            "start_date": "2022-07-01T00:00:00Z",
            "description": [
                "Led development of microservices architecture",
                "Improved system performance by 40%"
            ],
            "skills": ["Python", "FastAPI", "AWS", "Docker"]
        }
    })

class Resume(BaseModel):
    """
    Model representing a complete resume.
    
    Attributes:
        id: Unique identifier for the resume
        user_id: ID of the user who owns this resume
        full_name: Full name as shown on the resume
        email: Contact email address
        phone: Contact phone number (optional)
        location: Geographic location (optional)
        summary: Professional summary or objective (optional)
        skills: List of professional skills
        education: List of educational background
        experience: List of work experience
        created_at: When the resume was first created
        updated_at: When the resume was last updated
    """
    id: str = Field(..., description="Unique identifier for the resume")
    user_id: str = Field(..., description="ID of the user who owns this resume")
    full_name: str = Field(..., description="Full name as shown on the resume")
    email: str = Field(..., description="Contact email address")
    phone: Optional[str] = Field(None, description="Contact phone number")
    location: Optional[str] = Field(None, description="Geographic location")
    summary: Optional[str] = Field(None, description="Professional summary or objective")
    skills: List[str] = Field(default_factory=list, description="List of professional skills")
    education: List[Education] = Field(default_factory=list, description="List of educational background")
    experience: List[Experience] = Field(default_factory=list, description="List of work experience")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Resume creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "resume123",
            "user_id": "user123",
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "location": "San Francisco, CA",
            "summary": "Experienced software engineer with a focus on backend development",
            "skills": ["Python", "FastAPI", "AWS", "Docker"],
            "education": [{
                "institution": "Stanford University",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2018-09-01T00:00:00Z",
                "end_date": "2022-06-01T00:00:00Z",
                "gpa": 3.8
            }],
            "experience": [{
                "company": "Tech Corp",
                "title": "Senior Software Engineer",
                "location": "San Francisco, CA",
                "start_date": "2022-07-01T00:00:00Z",
                "description": [
                    "Led development of microservices architecture",
                    "Improved system performance by 40%"
                ],
                "skills": ["Python", "FastAPI", "AWS", "Docker"]
            }]
        }
    })

class ResumeCreate(BaseModel):
    """
    Model for creating a new resume from file upload.
    
    Attributes:
        file_content: Binary content of the uploaded resume file
        file_name: Name of the uploaded file
    """
    file_content: bytes = Field(..., description="Binary content of the uploaded resume file")
    file_name: str = Field(..., description="Name of the uploaded file")

class ResumeEnhancement(BaseModel):
    """
    Model for resume enhancement suggestions.
    
    Attributes:
        summary_suggestions: List of suggestions to improve the professional summary
        skill_suggestions: List of suggested skills to add
        experience_suggestions: List of suggestions to improve experience descriptions
        education_suggestions: List of suggestions to improve education section
    """
    summary_suggestions: List[str] = Field(..., description="Suggestions to improve the professional summary")
    skill_suggestions: List[str] = Field(..., description="Suggested skills to add")
    experience_suggestions: List[str] = Field(..., description="Suggestions to improve experience descriptions")
    education_suggestions: List[str] = Field(..., description="Suggestions to improve education section")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "summary_suggestions": [
                "Add quantifiable achievements",
                "Highlight leadership experience"
            ],
            "skill_suggestions": [
                "Kubernetes",
                "CI/CD",
                "System Design"
            ],
            "experience_suggestions": [
                "Add more specific metrics",
                "Include team size managed"
            ],
            "education_suggestions": [
                "Add relevant coursework",
                "Include academic projects"
            ]
        }
    })

class ResumeResponse(Resume):
    """
    Model for resume responses in API endpoints.
    Inherits all fields from the base Resume model.
    """
    pass
