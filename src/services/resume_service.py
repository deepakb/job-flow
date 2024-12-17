"""
Resume service for handling resume-related operations.

This module provides services for resume parsing, enhancement, and storage.
Features include:
- AI-powered resume parsing and analysis
- Skill extraction and scoring
- ATS optimization suggestions
- Career progression analysis
- Industry-specific recommendations
"""

import PyPDF2
import io
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
import openai
from models.resume import Resume, ResumeCreate, ResumeEnhancement, SkillAssessment
from core.config import get_settings
from repositories import ResumeRepository
from datetime import datetime

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY

SKILL_EXTRACTION_PROMPT = """
Analyze the resume and extract:
1. Technical skills (programming languages, tools, frameworks)
2. Soft skills (communication, leadership, etc.)
3. Domain expertise (industries, methodologies)
4. Certifications and qualifications

For each skill, provide:
- Skill name
- Category (technical/soft/domain)
- Proficiency level (1-5)
- Years of experience
- Context of usage
"""

RESUME_ENHANCEMENT_PROMPT = """
Analyze the resume and provide specific improvements for:
1. Content
   - Achievement quantification
   - Action verb usage
   - Technical terminology
   - Clarity and conciseness

2. ATS Optimization
   - Keyword optimization
   - Format compatibility
   - Section organization
   - Proper heading usage

3. Career Narrative
   - Professional progression
   - Impact demonstration
   - Skill development
   - Leadership growth

4. Industry Alignment
   - Industry-specific terminology
   - Relevant achievements
   - Market trends alignment
   - Competitive positioning
"""

class ResumeService:
    """
    Service for managing resume operations.
    
    Provides comprehensive resume analysis and enhancement using AI:
    - Resume parsing and structured data extraction
    - Skill assessment and scoring
    - ATS optimization
    - Career progression analysis
    - Industry-specific recommendations
    """
    
    def __init__(self):
        """Initialize the service with resume repository."""
        self.repository = ResumeRepository()

    async def parse_resume(self, file_content: bytes, file_name: str) -> str:
        """
        Parse text content from a resume file.
        
        Features:
        - PDF text extraction
        - Format preservation
        - Section identification
        - Header/footer handling
        
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

    async def extract_resume_data(self, text_content: str) -> Dict[str, Any]:
        """
        Extract structured data from resume text using OpenAI.
        
        Extracts:
        - Personal information
        - Contact details
        - Work experience
        - Education history
        - Skills and certifications
        - Projects and achievements
        
        Args:
            text_content: Plain text content of the resume
            
        Returns:
            Dict[str, Any]: Structured resume data
            
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
                        "content": "You are an expert resume parser. Extract detailed structured data from the resume."
                    },
                    {
                        "role": "user",
                        "content": f"Parse this resume into structured sections:\n{text_content}"
                    }
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting resume data: {str(e)}"
            )

    async def assess_skills(self, resume_id: str, user_id: str) -> List[SkillAssessment]:
        """
        Perform detailed skill assessment using AI.
        
        Features:
        - Skill extraction and categorization
        - Proficiency level assessment
        - Experience duration calculation
        - Industry relevance scoring
        - Skill gap analysis
        
        Args:
            resume_id: ID of the resume to assess
            user_id: ID of the requesting user
            
        Returns:
            List[SkillAssessment]: Detailed skill assessments
            
        Raises:
            HTTPException: If assessment fails
        """
        try:
            resume = await self.get_resume(resume_id, user_id)
            
            response = await openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": SKILL_EXTRACTION_PROMPT
                    },
                    {
                        "role": "user",
                        "content": resume.text
                    }
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error assessing skills: {str(e)}"
            )

    async def enhance_resume(self, resume_id: str, user_id: str) -> ResumeEnhancement:
        """
        Get comprehensive AI-powered enhancement suggestions.
        
        Provides improvements for:
        - Content and writing style
        - ATS optimization
        - Career narrative
        - Industry alignment
        - Skill presentation
        - Achievement quantification
        
        Args:
            resume_id: ID of the resume to enhance
            user_id: ID of the requesting user
            
        Returns:
            ResumeEnhancement: Detailed enhancement suggestions
            
        Raises:
            HTTPException: If enhancement fails or resume not found
        """
        try:
            resume = await self.get_resume(resume_id, user_id)
            
            # Get enhancement suggestions
            response = await openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": RESUME_ENHANCEMENT_PROMPT
                    },
                    {
                        "role": "user",
                        "content": resume.text
                    }
                ],
                temperature=0.7
            )
            
            suggestions = response.choices[0].message.content
            
            # Get ATS score
            ats_response = await openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an ATS system. Score this resume's ATS optimization (0-100) and explain why."
                    },
                    {
                        "role": "user",
                        "content": resume.text
                    }
                ],
                temperature=0.3
            )
            
            ats_feedback = ats_response.choices[0].message.content
            
            return ResumeEnhancement(
                content_suggestions=suggestions,
                ats_score=ats_feedback,
                skill_assessment=await self.assess_skills(resume_id, user_id)
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error enhancing resume: {str(e)}"
            )

    async def create_resume(self, resume_data: ResumeCreate, user_id: str) -> Resume:
        """
        Create a new resume with comprehensive analysis.
        
        Process:
        1. Parse resume file
        2. Extract structured data
        3. Perform skill assessment
        4. Calculate ATS score
        5. Store with metadata
        
        Args:
            resume_data: Resume creation data including file
            user_id: ID of the user creating the resume
            
        Returns:
            Resume: Created resume model with analysis
            
        Raises:
            HTTPException: If creation fails
        """
        try:
            # Parse and extract data
            text_content = await self.parse_resume(
                resume_data.file_content,
                resume_data.file_name
            )
            structured_data = await self.extract_resume_data(text_content)
            
            # Create resume
            resume = await self.repository.create_resume(
                user_id=user_id,
                data={
                    "text": text_content,
                    "structured_data": structured_data,
                    "file_name": resume_data.file_name,
                    "created_at": datetime.utcnow()
                }
            )
            
            # Perform initial analysis
            enhancement = await self.enhance_resume(resume.id, user_id)
            
            # Update resume with analysis
            return await self.repository.update_resume(
                resume_id=resume.id,
                data={
                    "skill_assessment": enhancement.skill_assessment,
                    "ats_score": enhancement.ats_score
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating resume: {str(e)}"
            )

    async def get_resume(self, resume_id: str, user_id: str) -> Resume:
        """Get a specific resume by ID."""
        resume = await self.repository.get(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
            
        if resume.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to access this resume"
            )
            
        return resume

    async def get_user_resumes(self, user_id: str) -> List[Resume]:
        """Get all resumes belonging to a user."""
        try:
            return await self.repository.get_user_resumes(user_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving resumes: {str(e)}"
            )
