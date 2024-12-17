"""
Application repository for managing job applications in Firestore.

This module implements the repository pattern for job application-related database operations.
It extends the base repository with application-specific functionality.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import BaseRepository
from models.application import JobApplication, ApplicationStatus

class ApplicationRepository(BaseRepository):
    """Repository for job application data management."""
    
    def __init__(self):
        """Initialize the application repository."""
        super().__init__('applications')
    
    async def create_application(
        self,
        user_id: str,
        job_id: str,
        resume_id: str,
        cover_letter: Optional[str] = None
    ) -> JobApplication:
        """Create a new job application."""
        now = datetime.utcnow()
        data = {
            'user_id': user_id,
            'job_id': job_id,
            'resume_id': resume_id,
            'cover_letter': cover_letter,
            'status': ApplicationStatus.DRAFT,
            'created_at': now,
            'updated_at': now,
            'submitted_at': None,
            'interview_date': None,
            'notes': None
        }
        doc_ref = await self.collection.add(data)
        data['id'] = doc_ref.id
        return JobApplication(**data)
    
    async def get_user_applications(
        self,
        user_id: str,
        status: Optional[ApplicationStatus] = None
    ) -> List[JobApplication]:
        """Get all applications submitted by a user."""
        query = self.collection.where('user_id', '==', user_id)
        if status:
            query = query.where('status', '==', status)
        docs = await query.get()
        return [self._convert_to_model(doc) for doc in docs]
    
    async def get_job_applications(
        self,
        job_id: str,
        status: Optional[ApplicationStatus] = None
    ) -> List[JobApplication]:
        """Get all applications for a specific job."""
        query = self.collection.where('job_id', '==', job_id)
        if status:
            query = query.where('status', '==', status)
        docs = await query.get()
        return [self._convert_to_model(doc) for doc in docs]
    
    async def update_application_status(
        self,
        application_id: str,
        status: ApplicationStatus,
        notes: Optional[str] = None
    ) -> Optional[JobApplication]:
        """Update the status of an application."""
        data = {
            'status': status,
            'updated_at': datetime.utcnow()
        }
        if notes:
            data['notes'] = notes
        if status == ApplicationStatus.SUBMITTED and not await self.get_field(application_id, 'submitted_at'):
            data['submitted_at'] = datetime.utcnow()
        
        success = await self.update(application_id, data)
        if success:
            return await self.get(application_id)
        return None
    
    async def get_application_with_details(
        self,
        application_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get an application with related job, user, and resume details."""
        application = await self.get(application_id)
        if not application:
            return None
        
        # Get related data (implement after other repositories are ready)
        return {
            'application': application,
            'job': None,  # TODO: Get job details
            'user': None,  # TODO: Get user details
            'resume': None  # TODO: Get resume details
        }
    
    def _convert_to_model(self, doc: Dict[str, Any]) -> JobApplication:
        """Convert Firestore document to JobApplication model."""
        data = doc.to_dict()
        data['id'] = doc.id
        return JobApplication(**data)
