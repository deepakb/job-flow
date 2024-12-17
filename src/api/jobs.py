from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List
from models.job import JobResponse, JobMatchResponse, JobSearch
from services.job_service import JobService
from services.user_service import UserService
from services.resume_service import ResumeService

router = APIRouter()
security = HTTPBearer()

@router.get("/search", response_model=List[JobResponse])
async def search_jobs(
    keyword: str = None,
    location: str = None,
    job_type: str = None,
    remote: bool = None,
    min_salary: int = None,
    max_salary: int = None,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    # Verify user
    user_service = UserService()
    await user_service.verify_token(credentials.credentials)

    # Create search parameters
    search_params = JobSearch(
        keyword=keyword,
        location=location,
        job_type=job_type,
        remote=remote,
        min_salary=min_salary,
        max_salary=max_salary
    )

    # Search jobs
    job_service = JobService()
    jobs = await job_service.search_jobs(search_params)
    return [JobResponse(**job.model_dump()) for job in jobs]

@router.get("/match/{resume_id}", response_model=List[JobMatchResponse])
async def match_jobs(
    resume_id: str,
    limit: int = 10,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    # Verify user
    user_service = UserService()
    token_data = await user_service.verify_token(credentials.credentials)
    
    # Get resume
    resume_service = ResumeService()
    resume = await resume_service.get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check if user owns the resume
    if resume.user_id != token_data['uid']:
        raise HTTPException(status_code=403, detail="Not authorized to use this resume")
    
    # Match jobs
    job_service = JobService()
    matches = await job_service.match_jobs(resume, limit)
    return [JobMatchResponse(**match.model_dump()) for match in matches]

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    # Verify user
    user_service = UserService()
    await user_service.verify_token(credentials.credentials)
    
    # Get job
    job_service = JobService()
    job = await job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobResponse(**job.model_dump())
