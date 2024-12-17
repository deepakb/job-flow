"""
Resume service for handling resume-related operations.

This module provides services for resume parsing, enhancement, and storage.
It uses OpenAI for text extraction and enhancement suggestions.
"""

import PyPDF2
import io
from typing import Optional, List
from fastapi import HTTPException
import openai
from models.resume import Resume, ResumeCreate, ResumeEnhancement
from core.config import get_settings
from repositories import ResumeRepository

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY

class ResumeService:
    """
    Service for managing resume operations.
    
    Handles resume parsing, data extraction, storage, and AI-powered enhancements.
    """
    
    def __init__(self):
        """Initialize the service with resume repository."""
        self.repository = ResumeRepository()

    async def parse_resume(self, file_content: bytes, file_name: str) -> str:
        """
        Parse text content from a resume file.
        
        Args:
            file_content: Binary content of the resume file
            file_name: Name of the uploaded file
            
        Returns:
            str: Extracted text content
            
        Raises:
            HTTPException: If parsing fails
        """
        try:
            # Parse PDF content
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            
            return text_content
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error parsing resume: {str(e)}"
            )

    async def extract_resume_data(self, text_content: str) -> dict:
        """
        Extract structured data from resume text using OpenAI.
        
        Args:
            text_content: Plain text content of the resume
            
        Returns:
            dict: Structured resume data
            
        Raises:
            HTTPException: If data extraction fails
        """
        try:
            # Use OpenAI to extract structured data
            response = await openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Extract structured resume data from the following text. Include: personal info, skills, education, and experience."
                    },
                    {"role": "user", "content": text_content}
                ]
            )
            
            structured_data = response.choices[0].message.content
            return structured_data
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting resume data: {str(e)}"
            )

    async def create_resume(self, resume_data: ResumeCreate, user_id: str) -> Resume:
        """
        Create a new resume for a user.
        
        Args:
            resume_data: Resume creation data including file
            user_id: ID of the user creating the resume
            
        Returns:
            Resume: Created resume model
            
        Raises:
            HTTPException: If resume creation fails
        """
        try:
            # Parse and extract data
            text_content = await self.parse_resume(
                resume_data.file_content,
                resume_data.file_name
            )
            structured_data = await self.extract_resume_data(text_content)
            
            # Create resume using repository
            return await self.repository.create_resume(user_id, structured_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating resume: {str(e)}"
            )

    async def enhance_resume(self, resume_id: str, user_id: str) -> ResumeEnhancement:
        """
        Get AI-powered enhancement suggestions for a resume.
        
        Args:
            resume_id: ID of the resume to enhance
            user_id: ID of the requesting user
            
        Returns:
            ResumeEnhancement: Enhancement suggestions
            
        Raises:
            HTTPException: If enhancement fails or resume not found
        """
        try:
            resume = await self.repository.get(resume_id)
            if not resume:
                raise HTTPException(
                    status_code=404,
                    detail="Resume not found"
                )
                
            if resume.user_id != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to access this resume"
                )

            # Use OpenAI to generate enhancement suggestions
            response = await openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze this resume and provide specific, actionable enhancement suggestions for each section."
                    },
                    {"role": "user", "content": resume.model_dump_json()}
                ]
            )
            
            suggestions = response.choices[0].message.content
            return ResumeEnhancement(
                summary_suggestions=suggestions.get('summary', []),
                skill_suggestions=suggestions.get('skills', []),
                experience_suggestions=suggestions.get('experience', []),
                education_suggestions=suggestions.get('education', [])
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error enhancing resume: {str(e)}"
            )

    async def get_resume(self, resume_id: str, user_id: str) -> Resume:
        """
        Get a specific resume by ID.
        
        Args:
            resume_id: ID of the resume to retrieve
            user_id: ID of the requesting user
            
        Returns:
            Resume: Retrieved resume
            
        Raises:
            HTTPException: If resume not found or user not authorized
        """
        resume = await self.repository.get(resume_id)
        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found"
            )
            
        if resume.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to access this resume"
            )
            
        return resume

    async def get_user_resumes(self, user_id: str) -> List[Resume]:
        """
        Get all resumes belonging to a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            List[Resume]: List of user's resumes
            
        Raises:
            HTTPException: If retrieval fails
        """
        try:
            return await self.repository.get_user_resumes(user_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving resumes: {str(e)}"
            )
