"""
Tests for user-related API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from main import app
from core.auth import create_access_token
from models.user import UserCreate, UserUpdate

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

class TestUserAPI:
    """Test cases for user-related endpoints."""

    def test_create_user(self, test_user):
        """Test user registration endpoint."""
        response = client.post("/api/users/register", json=test_user)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user["email"]
        assert data["full_name"] == test_user["full_name"]
        assert "id" in data
        assert "password" not in data

    def test_create_user_duplicate_email(self, test_user):
        """Test registration with duplicate email."""
        # First registration
        client.post("/api/users/register", json=test_user)
        
        # Duplicate registration
        response = client.post("/api/users/register", json=test_user)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_login(self, test_user):
        """Test user login endpoint."""
        # Create user first
        client.post("/api/users/register", json=test_user)
        
        # Test login
        response = client.post("/api/users/login", data={
            "username": test_user["email"],
            "password": test_user["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, test_user):
        """Test login with invalid credentials."""
        response = client.post("/api/users/login", data={
            "username": test_user["email"],
            "password": "wrongpass"
        })
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_get_current_user(self, test_user, auth_headers):
        """Test getting current user profile."""
        # Create user
        client.post("/api/users/register", json=test_user)
        
        # Get profile
        response = client.get("/api/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]
        assert data["full_name"] == test_user["full_name"]

    def test_update_user(self, test_user, auth_headers):
        """Test updating user profile."""
        # Create user
        client.post("/api/users/register", json=test_user)
        
        # Update profile
        update_data = {
            "full_name": "Updated Name",
            "phone": "+1234567890"
        }
        response = client.put("/api/users/me", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["phone"] == update_data["phone"]

    def test_delete_user(self, test_user, auth_headers):
        """Test user account deletion."""
        # Create user
        client.post("/api/users/register", json=test_user)
        
        # Delete account
        response = client.delete("/api/users/me", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify can't login anymore
        response = client.post("/api/users/login", data={
            "username": test_user["email"],
            "password": test_user["password"]
        })
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_password_reset(self, test_user):
        """Test password reset flow."""
        # Create user
        client.post("/api/users/register", json=test_user)
        
        # Request password reset
        response = client.post("/api/users/reset-password", json={
            "email": test_user["email"]
        })
        assert response.status_code == 200
        
        # Mock reset token
        reset_token = "mock_reset_token"
        
        # Reset password
        response = client.post(f"/api/users/reset-password/{reset_token}", json={
            "new_password": "newpass123"
        })
        assert response.status_code == 200
        
        # Verify can login with new password
        response = client.post("/api/users/login", data={
            "username": test_user["email"],
            "password": "newpass123"
        })
        assert response.status_code == 200
