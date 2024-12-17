"""
Tests for resume-related services.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import io
from datetime import datetime
from services.resume_service import ResumeService
from models.resume import ResumeCreate, Resume, ResumeEnhancement, SkillAssessment

@pytest.fixture
def resume_service():
    return ResumeService()

@pytest.fixture
def mock_pdf_content():
    return b"""
    John Doe
    Software Engineer
    
    Experience:
    - Senior Software Engineer at Tech Corp
    - Led development of microservices
    - Python, FastAPI, AWS expertise
    
    Education:
    - BS Computer Science, Stanford University
    """

@pytest.fixture
def mock_resume_data():
    return {
        "id": "test_resume_id",
        "user_id": "test_user_id",
        "file_name": "resume.pdf",
        "text": "Test resume content",
        "structured_data": {
            "personal_info": {"name": "John Doe"},
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp"
                }
            ]
        },
        "created_at": datetime.utcnow()
    }

class TestResumeService:
    """Test cases for ResumeService."""

    @pytest.mark.asyncio
    async def test_parse_resume(self, resume_service, mock_pdf_content):
        """Test resume parsing functionality."""
        result = await resume_service.parse_resume(mock_pdf_content, "test.pdf")
        assert isinstance(result, str)
        assert "John Doe" in result
        assert "Software Engineer" in result

    @pytest.mark.asyncio
    async def test_extract_resume_data(self, resume_service):
        """Test resume data extraction."""
        text_content = "John Doe\nSoftware Engineer\nPython, AWS"
        
        with patch('openai.ChatCompletion.create') as mock_openai:
            mock_openai.return_value.choices = [
                Mock(message=Mock(content={
                    "personal_info": {"name": "John Doe"},
                    "skills": ["Python", "AWS"]
                }))
            ]
            
            result = await resume_service.extract_resume_data(text_content)
            assert isinstance(result, dict)
            assert "personal_info" in str(result)
            assert "skills" in str(result)

    @pytest.mark.asyncio
    async def test_assess_skills(self, resume_service, mock_resume_data):
        """Test skill assessment functionality."""
        with patch('services.resume_service.ResumeService.get_resume') as mock_get:
            mock_get.return_value = Mock(**mock_resume_data)
            
            with patch('openai.ChatCompletion.create') as mock_openai:
                mock_openai.return_value.choices = [
                    Mock(message=Mock(content=[{
                        "name": "Python",
                        "category": "technical",
                        "proficiency": 5,
                        "years_experience": 3,
                        "context": "Used in backend development",
                        "relevance_score": 0.9
                    }]))
                ]
                
                result = await resume_service.assess_skills(
                    "test_resume_id",
                    "test_user_id"
                )
                assert "Python" in str(result)
                assert "technical" in str(result)

    @pytest.mark.asyncio
    async def test_enhance_resume(self, resume_service, mock_resume_data):
        """Test resume enhancement functionality."""
        with patch('services.resume_service.ResumeService.get_resume') as mock_get:
            mock_get.return_value = Mock(**mock_resume_data)
            
            with patch('openai.ChatCompletion.create') as mock_openai:
                mock_openai.return_value.choices = [
                    Mock(message=Mock(content={
                        "content_suggestions": {
                            "summary": ["Add more achievements"]
                        },
                        "ats_score": 85
                    }))
                ]
                
                result = await resume_service.enhance_resume(
                    "test_resume_id",
                    "test_user_id"
                )
                assert isinstance(result, ResumeEnhancement)
                assert "suggestions" in str(result.content_suggestions)
                assert result.ats_score is not None

    @pytest.mark.asyncio
    async def test_create_resume(self, resume_service, mock_pdf_content):
        """Test resume creation process."""
        resume_data = ResumeCreate(
            file_name="test.pdf",
            file_content=mock_pdf_content
        )
        
        with patch.multiple(
            resume_service,
            parse_resume=Mock(return_value="Test content"),
            extract_resume_data=Mock(return_value={"name": "John Doe"}),
            enhance_resume=Mock(return_value=ResumeEnhancement(
                content_suggestions={"summary": ["Add more"]},
                ats_score={"score": 85},
                skill_assessment=[
                    SkillAssessment(
                        name="Python",
                        category="technical",
                        proficiency=5,
                        years_experience=3,
                        context="Backend development",
                        relevance_score=0.9
                    )
                ]
            ))
        ):
            with patch.object(
                resume_service.repository,
                'create_resume',
                return_value=Mock(**mock_resume_data)
            ):
                result = await resume_service.create_resume(
                    resume_data,
                    "test_user_id"
                )
                assert isinstance(result, Resume)
                assert result.user_id == "test_user_id"
                assert result.file_name == "resume.pdf"

    @pytest.mark.asyncio
    async def test_get_resume(self, resume_service, mock_resume_data):
        """Test getting a specific resume."""
        with patch.object(
            resume_service.repository,
            'get',
            return_value=Mock(**mock_resume_data)
        ):
            result = await resume_service.get_resume(
                "test_resume_id",
                "test_user_id"
            )
            assert isinstance(result, Resume)
            assert result.id == "test_resume_id"
            assert result.user_id == "test_user_id"

    @pytest.mark.asyncio
    async def test_get_user_resumes(self, resume_service, mock_resume_data):
        """Test getting all resumes for a user."""
        with patch.object(
            resume_service.repository,
            'get_user_resumes',
            return_value=[Mock(**mock_resume_data)]
        ):
            result = await resume_service.get_user_resumes("test_user_id")
            assert isinstance(result, list)
            assert len(result) > 0
            assert result[0].user_id == "test_user_id"
