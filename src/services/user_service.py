"""
User service for handling user-related operations.

This module provides services for user management, including:
- User registration and authentication
- Profile management
- Token verification
"""

from typing import Optional
from models.user import UserCreate, UserUpdate, UserInDB
from repositories import UserRepository
from fastapi import HTTPException
from core.config import settings
from firebase_admin import auth

class UserService:
    """
    Service for managing user operations.
    
    Handles user registration, authentication, and profile management.
    """
    
    def __init__(self):
        """Initialize the service with user repository."""
        self.repository = UserRepository()

    async def create_user(self, user_data: UserCreate) -> UserInDB:
        """
        Create a new user with Firebase Authentication.
        
        Args:
            user_data: User creation data including email and password
            
        Returns:
            UserInDB: Created user model
            
        Raises:
            HTTPException: If user creation fails
        """
        try:
            # Create user with repository
            user_dict = user_data.model_dump()
            return await self.repository.create_with_auth(user_dict)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating user: {str(e)}"
            )

    async def get_user(self, user_id: str) -> UserInDB:
        """
        Get a user by ID.
        
        Args:
            user_id: ID of the user to retrieve
            
        Returns:
            UserInDB: User model
            
        Raises:
            HTTPException: If user not found or retrieval fails
        """
        try:
            user = await self.repository.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            return user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving user: {str(e)}"
            )

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Get a user by email address.
        
        Args:
            email: User's email address
            
        Returns:
            Optional[UserInDB]: User if found, None otherwise
            
        Raises:
            HTTPException: If retrieval fails
        """
        try:
            return await self.repository.get_by_email(email)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving user: {str(e)}"
            )

    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserInDB:
        """
        Update a user's profile.
        
        Args:
            user_id: ID of the user to update
            user_data: Update data
            
        Returns:
            UserInDB: Updated user model
            
        Raises:
            HTTPException: If user not found or update fails
        """
        try:
            # Get existing user to verify existence
            existing_user = await self.get_user(user_id)
            
            # Update only provided fields
            update_data = user_data.model_dump(exclude_unset=True)
            updated_user = await self.repository.update_profile(user_id, update_data)
            
            if not updated_user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
                
            return updated_user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating user: {str(e)}"
            )

    async def verify_token(self, token: str) -> dict:
        """
        Verify a Firebase ID token.
        
        Args:
            token: Firebase ID token to verify
            
        Returns:
            dict: Token claims including user ID
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            decoded_token = auth.verify_id_token(token)
            return {
                'user_id': decoded_token['uid'],
                'email': decoded_token.get('email'),
                'name': decoded_token.get('name')
            }
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )

    async def deactivate_user(self, user_id: str) -> UserInDB:
        """
        Deactivate a user account.
        
        Args:
            user_id: ID of the user to deactivate
            
        Returns:
            UserInDB: Deactivated user model
            
        Raises:
            HTTPException: If user not found or deactivation fails
        """
        try:
            deactivated_user = await self.repository.deactivate(user_id)
            if not deactivated_user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            return deactivated_user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deactivating user: {str(e)}"
            )
