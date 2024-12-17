"""
Resume repository for managing resume data in Firestore.

This module implements the repository pattern for resume-related database operations.
It extends the base repository with resume-specific functionality.
"""

from typing import Optional, List, Dict, Any
from .base import BaseRepository
from models.resume import Resume
from datetime import datetime
import json

class ResumeRepository(BaseRepository[Resume]):
    """
    Repository for resume data management.
    
    Extends the base repository with resume-specific operations and search capabilities.
    
    Attributes:
        collection_name: Name of the resumes collection in Firestore
    """
    
    def __init__(self):
        """Initialize the resume repository with the resumes collection."""
        super().__init__('resumes')

    async def get_user_resumes(self, user_id: str) -> List[Resume]:
        """
        Retrieve all resumes belonging to a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            List[Resume]: List of user's resumes
            
        Raises:
            FirestoreError: If query fails
        """
        return await self.find({'user_id': user_id})

    async def create_resume(self, user_id: str, resume_data: Dict[str, Any]) -> Resume:
        """
        Create a new resume for a user.
        
        Args:
            user_id: ID of the user
            resume_data: Dictionary containing resume data
            
        Returns:
            Resume: Created resume model
            
        Raises:
            FirestoreError: If document creation fails
        """
        resume_data['user_id'] = user_id
        return await self.create(resume_data)

    async def update_resume(self, resume_id: str, resume_data: Dict[str, Any]) -> Optional[Resume]:
        """
        Update an existing resume.
        
        Args:
            resume_id: ID of the resume to update
            resume_data: Dictionary containing update data
            
        Returns:
            Optional[Resume]: Updated resume if found, None otherwise
            
        Raises:
            FirestoreError: If update fails
        """
        return await self.update(resume_id, resume_data)

    async def search_resumes(
        self,
        filters: Dict[str, Any],
        limit: int = 20,
        offset: int = 0
    ) -> List[Resume]:
        """
        Search resumes with pagination.
        
        Args:
            filters: Dictionary of search filters
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            List[Resume]: List of matching resumes
            
        Raises:
            FirestoreError: If query fails
        """
        query = self.collection
        
        for field, value in filters.items():
            query = query.where(field, '==', value)
            
        query = query.offset(offset).limit(limit)
        docs = query.stream()
        
        return [self._convert_to_model(doc.to_dict()) for doc in docs]

    async def get_resume_with_user(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a resume with its associated user data.
        
        Args:
            resume_id: ID of the resume
            
        Returns:
            Optional[Dict[str, Any]]: Resume and user data if found, None otherwise
            
        Raises:
            FirestoreError: If query fails
        """
        resume = await self.get(resume_id)
        if not resume:
            return None
            
        user_doc = self.db.collection('users').document(resume.user_id).get()
        if not user_doc.exists:
            return None
            
        resume_dict = resume.model_dump()
        resume_dict['user'] = user_doc.to_dict()
        return resume_dict

    def _convert_to_model(self, data: Dict[str, Any]) -> Resume:
        """
        Convert dictionary data to Resume model.
        
        Args:
            data: Dictionary containing resume data
            
        Returns:
            Resume: Resume model instance
        """
        return Resume(**data)
