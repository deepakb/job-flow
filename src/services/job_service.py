from typing import List, Optional
import openai
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from fastapi import HTTPException

from models.job import Job, JobMatch, JobSearchParams
from models.resume import Resume
from repositories.firebase import FirebaseRepository
from core.config import get_settings

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY

class JobService:
    def __init__(self):
        self.repository = FirebaseRepository()

    async def scrape_jobs(self, source: str, keywords: List[str], location: Optional[str] = None) -> List[Job]:
        try:
            # Implementation of job scraping logic
            pass
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error scraping jobs: {str(e)}"
            )

    async def search_jobs(
        self,
        params: JobSearchParams,
        offset: int = 0,
        limit: int = 20
    ) -> List[Job]:
        """
        Search for jobs based on specified parameters.
        
        Args:
            params: Search parameters including keywords and filters
            offset: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            List[Job]: List of matching jobs
        """
        try:
            jobs = await self.repository.search_jobs(
                keywords=params.keywords,
                location=params.location,
                job_type=params.job_type,
                experience_level=params.experience_level,
                remote=params.remote,
                offset=offset,
                limit=limit
            )
            return jobs
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error searching jobs: {str(e)}"
            )

    async def get_job_matches(
        self,
        resume_id: str,
        offset: int = 0,
        limit: int = 20
    ) -> List[JobMatch]:
        """
        Get job recommendations based on a resume.
        
        Args:
            resume_id: ID of the resume to match against
            offset: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            List[JobMatch]: List of job matches with scores
        """
        try:
            resume = await self.repository.get_resume(resume_id)
            if not resume:
                raise HTTPException(
                    status_code=404,
                    detail="Resume not found"
                )

            # Get job matches using OpenAI
            matches = await self._get_matches_with_openai(resume)
            
            # Sort by match score and apply pagination
            matches.sort(key=lambda x: x.match_score, reverse=True)
            return matches[offset:offset + limit]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting job matches: {str(e)}"
            )

    async def get_job(self, job_id: str) -> Optional[Job]:
        """
        Get detailed information about a specific job.
        
        Args:
            job_id: ID of the job to retrieve
            
        Returns:
            Optional[Job]: Job details if found, None otherwise
        """
        try:
            job = await self.repository.get_job(job_id)
            if not job:
                raise HTTPException(
                    status_code=404,
                    detail="Job not found"
                )
            return job
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting job: {str(e)}"
            )

    async def _get_matches_with_openai(self, resume: Resume) -> List[JobMatch]:
        """
        Use OpenAI to get job matches for a resume.
        
        Args:
            resume: Resume to match against jobs
            
        Returns:
            List[JobMatch]: List of job matches with scores
        """
        try:
            # Get all available jobs
            jobs = await self.repository.get_all_jobs()
            
            matches = []
            for job in jobs:
                # Use OpenAI to calculate match score
                response = await openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a job matching expert."},
                        {"role": "user", "content": f"Calculate match score between resume and job:\nResume: {resume.text}\nJob: {job.description}"}
                    ]
                )
                
                # Parse match score from response
                match_score = float(response.choices[0].message.content)
                
                matches.append(JobMatch(
                    job=job,
                    match_score=match_score,
                    matching_skills=[],  # TODO: Extract matching skills
                    missing_skills=[]    # TODO: Extract missing skills
                ))
            
            return matches
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error matching with OpenAI: {str(e)}"
            )
