"""
Job API endpoints.

This module provides API endpoints for job-related operations, including:
- Job search and filtering
- Job recommendations and matching
- Job application management
- Job details retrieval
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from models.job import JobResponse, JobMatchResponse, JobSearchParams
from models.application import JobApplication
from services.job_service import JobService
from core.auth import get_current_user_id

router = APIRouter()

@router.get("/search",
    response_model=List[JobResponse],
    summary="Search for jobs",
    description="""
    Search for jobs based on various criteria.
    
    You can filter jobs by:
    * Keywords (job title, company, description)
    * Location
    * Remote work preference
    * Salary requirements
    * Job type (full-time, part-time, contract)
    * Experience level
    * Required skills
    
    Results are sorted by relevance and posting date.
    Pagination is supported through offset and limit parameters.
    """,
    response_description="List of matching jobs",
    responses={
        200: {
            "description": "Successful search results",
            "content": {
                "application/json": {
                    "example": [{
                        "id": "job123",
                        "title": "Senior Backend Engineer",
                        "company_name": "Tech Corp",
                        "location": {
                            "city": "San Francisco",
                            "state": "California",
                            "is_remote": True
                        },
                        "posted_at": "2024-12-17T13:30:00Z"
                    }]
                }
            }
        },
        401: {"description": "Invalid or expired token"},
        422: {"description": "Invalid search parameters"}
    }
) 
async def search_jobs(
    params: JobSearchParams,
    offset: int = Query(0, description="Number of items to skip"),
    limit: int = Query(20, description="Maximum number of items to return"),
    credentials: str = Depends(get_current_user_id)
) -> List[JobResponse]:
    """
    Search for jobs based on specified criteria.
    
    Args:
        params: Search parameters including keywords, location, and filters
        offset: Number of items to skip for pagination
        limit: Maximum number of items to return
        credentials: User's JWT token for authentication
        
    Returns:
        List[JobResponse]: List of matching jobs with details
        
    Raises:
        HTTPException: If search parameters are invalid or authentication fails
    """
    service = JobService()
    return await service.search_jobs(params, offset=offset, limit=limit)

@router.get("/matches/{resume_id}",
    response_model=List[JobMatchResponse],
    summary="Get job recommendations",
    description="""
    Get personalized job recommendations based on a user's resume.
    
    The matching algorithm considers:
    * Skills and technologies
    * Experience level
    * Job preferences
    * Location preferences
    * Salary expectations
    
    Results include a match score and detailed comparison.
    Pagination is supported through offset and limit parameters.
    """,
    response_description="List of job matches with scores",
    responses={
        200: {
            "description": "Successful matches found",
            "content": {
                "application/json": {
                    "example": [{
                        "job": {
                            "id": "job123",
                            "title": "Senior Backend Engineer"
                        },
                        "match_score": 0.85,
                        "matching_skills": ["Python", "FastAPI"],
                        "missing_skills": ["GraphQL"]
                    }]
                }
            }
        },
        401: {"description": "Invalid or expired token"},
        404: {"description": "Resume not found"},
        422: {"description": "Invalid resume format"}
    }
)
async def get_job_matches(
    resume_id: str,
    offset: int = Query(0, description="Number of items to skip"),
    limit: int = Query(20, description="Maximum number of items to return"),
    credentials: str = Depends(get_current_user_id)
) -> List[JobMatchResponse]:
    """
    Get job recommendations based on a resume.
    
    Args:
        resume_id: ID of the resume to match against
        offset: Number of items to skip for pagination
        limit: Maximum number of items to return
        credentials: User's JWT token for authentication
        
    Returns:
        List[JobMatchResponse]: List of matching jobs with scores
        
    Raises:
        HTTPException: If resume not found or not authorized
    """
    service = JobService()
    return await service.get_job_matches(resume_id, offset=offset, limit=limit)

@router.get("/{job_id}",
    response_model=JobResponse,
    summary="Get job details",
    description="""
    Get detailed information about a specific job posting.
    
    Returns comprehensive job details including:
    * Job description and requirements
    * Company information
    * Location and remote work options
    * Compensation and benefits
    * Application instructions
    * Posted date and deadline
    """,
    response_description="Detailed job information",
    responses={
        200: {
            "description": "Job details found",
            "content": {
                "application/json": {
                    "example": {
                        "id": "job123",
                        "title": "Senior Backend Engineer",
                        "company_name": "Tech Corp",
                        "description": "We are seeking...",
                        "requirements": ["Python", "FastAPI"],
                        "posted_at": "2024-12-17T13:30:00Z"
                    }
                }
            }
        },
        401: {"description": "Invalid or expired token"},
        404: {"description": "Job not found"}
    }
)
async def get_job(
    job_id: str,
    credentials: str = Depends(get_current_user_id)
) -> JobResponse:
    """
    Get detailed information about a specific job.
    
    Args:
        job_id: ID of the job to retrieve
        credentials: User's JWT token for authentication
        
    Returns:
        JobResponse: Detailed job information
        
    Raises:
        HTTPException: If job not found or authentication fails
    """
    service = JobService()
    return await service.get_job(job_id)

@router.post("/{job_id}/apply",
    response_model=JobApplication,
    summary="Apply for a job",
    description="""
    Submit a job application for a specific position.
    
    Required:
    * Valid resume
    * Authorization to apply
    
    Optional:
    * Cover letter
    * Additional notes
    
    The application will be tracked and status updates will be sent.
    """,
    response_description="Application submission details",
    responses={
        201: {
            "description": "Application submitted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "app123",
                        "job_id": "job123",
                        "status": "submitted",
                        "submitted_at": "2024-12-17T13:30:00Z"
                    }
                }
            }
        },
        401: {"description": "Invalid or expired token"},
        404: {"description": "Job or resume not found"},
        409: {"description": "Already applied to this job"},
        422: {"description": "Invalid application data"}
    }
)
async def apply_for_job(
    job_id: str,
    resume_id: str,
    cover_letter: Optional[str] = None,
    credentials: str = Depends(get_current_user_id)
) -> JobApplication:
    """
    Submit a job application.
    
    Args:
        job_id: ID of the job to apply for
        resume_id: ID of the resume to use
        cover_letter: Optional cover letter text
        credentials: User's JWT token for authentication
        
    Returns:
        JobApplication: Application submission details
        
    Raises:
        HTTPException: If job not found, resume not authorized, or already applied
    """
    service = JobService()
    return await service.apply_for_job(
        job_id=job_id,
        resume_id=resume_id,
        user_id=credentials,
        cover_letter=cover_letter
    )
