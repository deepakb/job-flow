"""
User repository for managing user data in Firestore.

This module implements the repository pattern for user-related database operations.
It extends the base repository with user-specific functionality.
"""

from typing import Optional, List, Dict, Any
from .base import BaseRepository
from models.user import UserInDB
from firebase_admin import auth
from core.config import settings

class UserRepository(BaseRepository[UserInDB]):
    """
    Repository for user data management.
    
    Extends the base repository with user-specific operations and Firebase
    Authentication integration.
    
    Attributes:
        collection_name: Name of the users collection in Firestore
    """
    
    def __init__(self):
        """Initialize the user repository with the users collection."""
        super().__init__('users')

    async def create_with_auth(self, user_data: Dict[str, Any]) -> UserInDB:
        """
        Create a new user with Firebase Authentication.
        
        Creates both a Firebase Auth user and a Firestore document.
        
        Args:
            user_data: Dictionary containing user data including email and password
            
        Returns:
            UserInDB: Created user model
            
        Raises:
            FirebaseError: If user creation in Firebase Auth fails
            FirestoreError: If document creation fails
        """
        # Create Firebase Auth user
        auth_user = auth.create_user(
            email=user_data['email'],
            password=user_data['password'],
            display_name=user_data['name']
        )
        
        # Remove password before storing in Firestore
        user_data.pop('password', None)
        user_data['id'] = auth_user.uid
        
        # Create Firestore document
        return await self.create(user_data)

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Retrieve a user by email address.
        
        Args:
            email: User's email address
            
        Returns:
            Optional[UserInDB]: User if found, None otherwise
            
        Raises:
            FirestoreError: If query fails
        """
        users = await self.find({'email': email})
        return users[0] if users else None

    async def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Optional[UserInDB]:
        """
        Update a user's profile information.
        
        Args:
            user_id: User's ID
            profile_data: Dictionary containing profile updates
            
        Returns:
            Optional[UserInDB]: Updated user if found, None otherwise
            
        Raises:
            FirestoreError: If update fails
        """
        # Update Firebase Auth display name if provided
        if 'name' in profile_data:
            auth.update_user(
                user_id,
                display_name=profile_data['name']
            )
        
        return await self.update(user_id, profile_data)

    async def verify_email(self, user_id: str) -> Optional[UserInDB]:
        """
        Mark a user's email as verified.
        
        Args:
            user_id: User's ID
            
        Returns:
            Optional[UserInDB]: Updated user if found, None otherwise
            
        Raises:
            FirestoreError: If update fails
        """
        return await self.update(user_id, {'is_verified': True})

    async def deactivate(self, user_id: str) -> Optional[UserInDB]:
        """
        Deactivate a user account.
        
        Disables the user in Firebase Auth and marks them as inactive in Firestore.
        
        Args:
            user_id: User's ID
            
        Returns:
            Optional[UserInDB]: Updated user if found, None otherwise
            
        Raises:
            FirebaseError: If Firebase Auth update fails
            FirestoreError: If Firestore update fails
        """
        # Disable Firebase Auth account
        auth.update_user(
            user_id,
            disabled=True
        )
        
        return await self.update(user_id, {'is_active': False})

    def _convert_to_model(self, data: Dict[str, Any]) -> UserInDB:
        """
        Convert dictionary data to UserInDB model.
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            UserInDB: User model instance
        """
        return UserInDB(**data)
