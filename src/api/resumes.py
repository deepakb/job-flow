"""
Resume API endpoints.

This module provides API endpoints for resume management, including:
- Resume upload and parsing
- Resume retrieval
- AI-powered resume enhancement
"""

from fastapi import APIRouter, Depends, HTTPException, Security, UploadFile, File, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.resume import ResumeCreate, ResumeResponse, ResumeEnhancement
from services.resume_service import ResumeService
from typing import List
from core.auth import get_current_user_id

router = APIRouter()
security = HTTPBearer()

@router.post("/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new resume",
    description="""
    Upload and parse a new resume document.
    
    Supported file formats:
    * PDF (.pdf)
    * Microsoft Word (.doc, .docx)
    * Plain Text (.txt)
    
    The resume will be parsed to extract structured information including:
    * Personal information
    * Work experience
    * Education
    * Skills
    """,
    response_description="The parsed resume data",
    responses={
        201: {
            "description": "Resume successfully uploaded and parsed",
            "content": {
                "application/json": {
                    "example": {
                        "id": "resume123",
                        "user_id": "user123",
                        "full_name": "John Doe",
                        "email": "john.doe@example.com",
                        "skills": ["Python", "FastAPI"],
                        "created_at": "2024-12-17T13:30:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Invalid file format or parsing error",
            "content": {
                "application/json": {
                    "example": {"detail": "Unsupported file format"}
                }
            }
        },
        401: {"description": "Invalid or expired token"},
        403: {"description": "Not authorized to perform this action"}
    }
)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
) -> ResumeResponse:
    """
    Upload and parse a new resume document.
    
    Args:
        file: The resume file to upload
        user_id: ID of the current user from token
        
    Returns:
        ResumeResponse: The parsed resume data
        
    Raises:
        HTTPException: If file format is invalid or parsing fails
    """
    service = ResumeService()
    content = await file.read()
    resume_data = ResumeCreate(
        file_content=content,
        file_name=file.filename
    )
    resume = await service.create_resume(resume_data, user_id)
    return ResumeResponse(**resume.model_dump())

@router.get("/me",
    response_model=List[ResumeResponse],
    summary="Get user's resumes",
    description="Retrieve all resumes belonging to the currently authenticated user.",
    response_description="List of user's resumes",
    responses={
        401: {"description": "Invalid or expired token"},
        403: {"description": "Not authorized to perform this action"},
        404: {"description": "No resumes found"}
    }
)
async def get_user_resumes(
    user_id: str = Depends(get_current_user_id)
) -> List[ResumeResponse]:
    """
    Get all resumes belonging to the current user.
    
    Args:
        user_id: ID of the current user from token
        
    Returns:
        List[ResumeResponse]: List of user's resumes
        
    Raises:
        HTTPException: If retrieval fails
    """
    service = ResumeService()
    resumes = await service.get_user_resumes(user_id)
    return [ResumeResponse(**resume.model_dump()) for resume in resumes]

@router.get("/{resume_id}",
    response_model=ResumeResponse,
    summary="Get resume by ID",
    description="Retrieve a specific resume by its ID. Only accessible by the resume owner.",
    response_description="The requested resume",
    responses={
        401: {"description": "Invalid or expired token"},
        403: {"description": "Not authorized to access this resume"},
        404: {"description": "Resume not found"}
    }
)
async def get_resume(
    resume_id: str,
    user_id: str = Depends(get_current_user_id)
) -> ResumeResponse:
    """
    Get a specific resume by its ID.
    
    Args:
        resume_id: ID of the resume to retrieve
        user_id: ID of the current user from token
        
    Returns:
        ResumeResponse: The requested resume
        
    Raises:
        HTTPException: If resume not found or user not authorized
    """
    service = ResumeService()
    resume = await service.get_resume(resume_id, user_id)
    return ResumeResponse(**resume.model_dump())

@router.post("/{resume_id}/enhance",
    response_model=ResumeEnhancement,
    summary="Enhance resume",
    description="""
    Get AI-powered suggestions to enhance a resume.
    
    The enhancement includes suggestions for:
    * Professional summary
    * Skills presentation
    * Work experience descriptions
    * Education details
    """,
    response_description="Enhancement suggestions for the resume",
    responses={
        401: {"description": "Invalid or expired token"},
        403: {"description": "Not authorized to access this resume"},
        404: {"description": "Resume not found"}
    }
)
async def enhance_resume(
    resume_id: str,
    user_id: str = Depends(get_current_user_id)
) -> ResumeEnhancement:
    """
    Get AI-powered suggestions to enhance a resume.
    
    Args:
        resume_id: ID of the resume to enhance
        user_id: ID of the current user from token
        
    Returns:
        ResumeEnhancement: Suggestions for improving the resume
        
    Raises:
        HTTPException: If resume not found or user not authorized
    """
    service = ResumeService()
    return await service.enhance_resume(resume_id, user_id)
