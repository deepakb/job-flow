"""
User API endpoints.

This module provides API endpoints for user management, including:
- User registration and authentication
- Profile management and updates
- Account deactivation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from models.user import UserCreate, UserUpdate, UserResponse, Token
from services.user_service import UserService
from core.auth import get_current_user_id

router = APIRouter()

@router.post("/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="""
    Register a new user account with the provided information.
    
    The user must provide:
    - A valid email address
    - A secure password (minimum 8 characters)
    - Their full name
    - Optional: Professional skills and job preferences
    
    Returns the created user profile without sensitive information.
    """
)
async def register_user(user_data: UserCreate) -> UserResponse:
    """
    Register a new user account.

    Args:
        user_data: User registration information including email, password, and profile details

    Returns:
        UserResponse: Created user profile

    Raises:
        HTTPException: If email is already registered or validation fails
    """
    service = UserService()
    user = await service.create_user(user_data)
    return UserResponse(**user.model_dump())

@router.get("/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="""
    Retrieve the complete profile of the currently authenticated user.
    
    Returns:
    - Personal information (name, email)
    - Professional details (skills, experience)
    - Account settings and preferences
    
    Requires authentication via JWT token.
    """
)
async def get_current_user(user_id: str = Depends(get_current_user_id)) -> UserResponse:
    """
    Get the current user's profile.

    Args:
        user_id: ID of the authenticated user (from JWT token)

    Returns:
        UserResponse: Complete user profile

    Raises:
        HTTPException: If user is not found or authentication fails
    """
    service = UserService()
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.model_dump())

@router.patch("/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="""
    Update the profile information of the currently authenticated user.
    
    Updatable fields:
    - Name
    - Professional skills
    - Job preferences
    - Profile settings
    
    Only provided fields will be updated. Requires authentication.
    """
)
async def update_current_user(
    user_data: UserUpdate,
    user_id: str = Depends(get_current_user_id)
) -> UserResponse:
    """
    Update the current user's profile.

    Args:
        user_data: Fields to update in the user's profile
        user_id: ID of the authenticated user (from JWT token)

    Returns:
        UserResponse: Updated user profile

    Raises:
        HTTPException: If user is not found or validation fails
    """
    service = UserService()
    updated_user = await service.update_user(user_id, user_data)
    return UserResponse(**updated_user.model_dump())

@router.post("/me/deactivate",
    response_model=UserResponse,
    summary="Deactivate current user account",
    description="""
    Deactivate the currently authenticated user's account.
    
    Effects:
    - Account becomes inactive
    - User can no longer log in
    - Active job applications are withdrawn
    - Profile becomes hidden from job matches
    
    This action can be reversed by contacting support.
    Requires authentication.
    """
)
async def deactivate_current_user(user_id: str = Depends(get_current_user_id)) -> UserResponse:
    """
    Deactivate the current user's account.

    Args:
        user_id: ID of the authenticated user (from JWT token)

    Returns:
        UserResponse: Deactivated user profile

    Raises:
        HTTPException: If user is not found or already deactivated
    """
    service = UserService()
    deactivated_user = await service.deactivate_user(user_id)
    return UserResponse(**deactivated_user.model_dump())
