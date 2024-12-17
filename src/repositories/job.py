"""
Job repository for managing job data in Firestore.

This module implements the repository pattern for job-related database operations.
It extends the base repository with job-specific functionality.
"""

from typing import Optional, List, Dict, Any
from .base import BaseRepository
from models.job import Job
from datetime import datetime

class JobRepository(BaseRepository[Job]):
    """
    Repository for job data management.
    
    Extends the base repository with job-specific operations and search capabilities.
    
    Attributes:
        collection_name: Name of the jobs collection in Firestore
    """
    
    def __init__(self):
        """Initialize the job repository with the jobs collection."""
        super().__init__('jobs')

    async def search_jobs(
        self,
        filters: Dict[str, Any],
        sort_by: str = 'created_at',
        sort_desc: bool = True,
        limit: int = 20,
        offset: int = 0
    ) -> List[Job]:
        """
        Search jobs with filters, sorting, and pagination.
        
        Args:
            filters: Dictionary of search filters
            sort_by: Field to sort by
            sort_desc: Sort in descending order if True
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            List[Job]: List of matching jobs
            
        Raises:
            FirestoreError: If query fails
        """
        query = self.collection
        
        for field, value in filters.items():
            query = query.where(field, '==', value)
            
        query = query.order_by(
            sort_by, 
            direction='DESCENDING' if sort_desc else 'ASCENDING'
        )
        
        query = query.offset(offset).limit(limit)
        docs = query.stream()
        
        return [self._convert_to_model(doc.to_dict()) for doc in docs]

    async def get_company_jobs(
        self,
        company_id: str,
        status: str = 'active'
    ) -> List[Job]:
        """
        Get all jobs posted by a company.
        
        Args:
            company_id: ID of the company
            status: Job status filter
            
        Returns:
            List[Job]: List of company's jobs
            
        Raises:
            FirestoreError: If query fails
        """
        return await self.find({
            'company_id': company_id,
            'status': status
        })

    async def update_job_status(
        self,
        job_id: str,
        status: str,
        reason: Optional[str] = None
    ) -> Optional[Job]:
        """
        Update a job's status.
        
        Args:
            job_id: ID of the job
            status: New status value
            reason: Optional reason for status change
            
        Returns:
            Optional[Job]: Updated job if found, None otherwise
            
        Raises:
            FirestoreError: If update fails
        """
        update_data = {
            'status': status,
            'status_updated_at': datetime.utcnow()
        }
        
        if reason:
            update_data['status_reason'] = reason
            
        return await self.update(job_id, update_data)

    async def get_similar_jobs(
        self,
        job_id: str,
        limit: int = 5
    ) -> List[Job]:
        """
        Get similar jobs based on title and skills.
        
        Args:
            job_id: ID of the reference job
            limit: Maximum number of similar jobs to return
            
        Returns:
            List[Job]: List of similar jobs
            
        Raises:
            FirestoreError: If query fails
        """
        job = await self.get(job_id)
        if not job:
            return []
            
        # Query jobs with matching skills
        query = self.collection
        query = query.where('skills', 'array_contains_any', job.skills)
        query = query.where('id', '!=', job_id)
        query = query.limit(limit)
        
        docs = query.stream()
        return [self._convert_to_model(doc.to_dict()) for doc in docs]

    def _convert_to_model(self, data: Dict[str, Any]) -> Job:
        """
        Convert dictionary data to Job model.
        
        Args:
            data: Dictionary containing job data
            
        Returns:
            Job: Job model instance
        """
        return Job(**data)
