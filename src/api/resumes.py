from fastapi import APIRouter, Depends, HTTPException, Security, UploadFile, File
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List
from models.resume import Resume, ResumeEnhancement, ResumeResponse
from services.resume_service import ResumeService
from services.user_service import UserService

router = APIRouter()
security = HTTPBearer()

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    user_service = UserService()
    resume_service = ResumeService()

    # Verify user
    token_data = await user_service.verify_token(credentials.credentials)
    user_id = token_data['uid']

    # Read and parse resume
    content = await file.read()
    text_content = await resume_service.parse_resume(content, file.filename)
    
    # Extract structured data
    resume_data = await resume_service.extract_resume_data(text_content)
    
    # Store resume
    resume = await resume_service.store_resume(user_id, resume_data)
    return ResumeResponse(**resume.model_dump())

@router.get("/me", response_model=List[ResumeResponse])
async def get_my_resumes(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    user_service = UserService()
    resume_service = ResumeService()

    # Verify user
    token_data = await user_service.verify_token(credentials.credentials)
    user_id = token_data['uid']

    # Get user's resumes
    resumes = await resume_service.get_user_resumes(user_id)
    return [ResumeResponse(**resume.model_dump()) for resume in resumes]

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    user_service = UserService()
    resume_service = ResumeService()

    # Verify user
    token_data = await user_service.verify_token(credentials.credentials)
    
    # Get resume
    resume = await resume_service.get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check if user owns the resume
    if resume.user_id != token_data['uid']:
        raise HTTPException(status_code=403, detail="Not authorized to access this resume")
    
    return ResumeResponse(**resume.model_dump())

@router.post("/{resume_id}/enhance", response_model=ResumeEnhancement)
async def enhance_resume(
    resume_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    user_service = UserService()
    resume_service = ResumeService()

    # Verify user
    token_data = await user_service.verify_token(credentials.credentials)
    
    # Get resume
    resume = await resume_service.get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check if user owns the resume
    if resume.user_id != token_data['uid']:
        raise HTTPException(status_code=403, detail="Not authorized to enhance this resume")
    
    # Get enhancement suggestions
    enhancements = await resume_service.enhance_resume(resume_id)
    return enhancements
