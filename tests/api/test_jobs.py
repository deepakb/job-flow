"""
Tests for job-related API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from main import app
from models.job import JobCreate, JobUpdate, JobSearchParams
from core.auth import create_access_token

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token(
        data={"sub": test_user["email"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def test_job():
    return {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "location": "San Francisco, CA",
        "description": "Looking for an experienced software engineer...",
        "requirements": ["Python", "FastAPI", "AWS"],
        "salary_range": {"min": 120000, "max": 180000},
        "job_type": "full-time",
        "remote": True
    }

class TestJobsAPI:
    """Test cases for job-related endpoints."""

    def test_create_job(self, test_user, auth_headers, test_job):
        """Test job creation endpoint."""
        response = client.post("/api/jobs/", json=test_job, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == test_job["title"]
        assert data["company"] == test_job["company"]
        assert "id" in data

    def test_get_job(self, test_user, auth_headers, test_job):
        """Test getting a specific job."""
        # Create job first
        create_response = client.post("/api/jobs/", json=test_job, headers=auth_headers)
        job_id = create_response.json()["id"]
        
        # Get job
        response = client.get(f"/api/jobs/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_job["title"]
        assert data["company"] == test_job["company"]

    def test_search_jobs(self, test_user, auth_headers, test_job):
        """Test job search functionality."""
        # Create test job
        client.post("/api/jobs/", json=test_job, headers=auth_headers)
        
        # Test search
        search_params = {
            "keyword": "software engineer",
            "location": "San Francisco",
            "remote": True,
            "job_type": "full-time",
            "min_salary": 100000
        }
        response = client.get("/api/jobs/search", params=search_params)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert any(job["title"] == test_job["title"] for job in data)

    def test_update_job(self, test_user, auth_headers, test_job):
        """Test job update endpoint."""
        # Create job
        create_response = client.post("/api/jobs/", json=test_job, headers=auth_headers)
        job_id = create_response.json()["id"]
        
        # Update job
        update_data = {
            "title": "Lead Software Engineer",
            "salary_range": {"min": 140000, "max": 200000}
        }
        response = client.put(
            f"/api/jobs/{job_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["salary_range"] == update_data["salary_range"]

    def test_delete_job(self, test_user, auth_headers, test_job):
        """Test job deletion."""
        # Create job
        create_response = client.post("/api/jobs/", json=test_job, headers=auth_headers)
        job_id = create_response.json()["id"]
        
        # Delete job
        response = client.delete(f"/api/jobs/{job_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify job is deleted
        response = client.get(f"/api/jobs/{job_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_apply_for_job(self, test_user, auth_headers, test_job):
        """Test job application process."""
        # Create job
        create_response = client.post("/api/jobs/", json=test_job, headers=auth_headers)
        job_id = create_response.json()["id"]
        
        # Apply for job
        application_data = {
            "cover_letter": "I am very interested in this position...",
            "resume_id": "test_resume_id"
        }
        response = client.post(
            f"/api/jobs/{job_id}/apply",
            json=application_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["job_id"] == job_id
        assert data["status"] == "pending"

    def test_get_job_applications(self, test_user, auth_headers, test_job):
        """Test retrieving job applications."""
        # Create job and apply
        create_response = client.post("/api/jobs/", json=test_job, headers=auth_headers)
        job_id = create_response.json()["id"]
        
        application_data = {
            "cover_letter": "I am very interested...",
            "resume_id": "test_resume_id"
        }
        client.post(
            f"/api/jobs/{job_id}/apply",
            json=application_data,
            headers=auth_headers
        )
        
        # Get applications
        response = client.get("/api/jobs/applications", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["job_id"] == job_id

    @pytest.mark.asyncio
    async def test_job_recommendations(self, test_user, auth_headers):
        """Test job recommendations endpoint."""
        response = client.get("/api/jobs/recommendations", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert all(isinstance(job, dict) for job in data)
            assert all("title" in job for job in data)
            assert all("relevance_score" in job for job in data)
