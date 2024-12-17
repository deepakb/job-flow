from typing import List, Optional
import openai
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from fastapi import HTTPException

from models.job import Job, JobMatch, JobSearch
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
            jobs = []
            if source.lower() == "linkedin":
                # Example LinkedIn scraping (you'd need to implement proper scraping logic)
                url = f"https://www.linkedin.com/jobs/search?keywords={'%20'.join(keywords)}"
                if location:
                    url += f"&location={location}"
                
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                # Implement LinkedIn specific scraping logic
                
            elif source.lower() == "indeed":
                # Implement Indeed scraping logic
                pass
            
            # Store scraped jobs
            for job_data in jobs:
                await self.store_job(job_data)
            
            return jobs
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error scraping jobs: {str(e)}")

    async def store_job(self, job_data: dict) -> Job:
        try:
            # Add timestamps
            job_data["created_at"] = datetime.utcnow()
            job_data["updated_at"] = datetime.utcnow()
            
            # Store in Firestore
            doc_ref = await self.repository.create_document("jobs", job_data)
            return Job(id=doc_ref.id, **job_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error storing job: {str(e)}")

    async def search_jobs(self, search_params: JobSearch) -> List[Job]:
        try:
            # Build query conditions
            conditions = []
            if search_params.keyword:
                conditions.append(("title", "contains", search_params.keyword))
            if search_params.location:
                conditions.append(("location", "==", search_params.location))
            if search_params.job_type:
                conditions.append(("job_type", "==", search_params.job_type))
            if search_params.remote is not None:
                conditions.append(("remote", "==", search_params.remote))
            
            # Query Firestore
            jobs_data = await self.repository.query_documents("jobs", conditions)
            return [Job(**job_data) for job_data in jobs_data]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching jobs: {str(e)}")

    async def match_jobs(self, resume: Resume, limit: int = 10) -> List[JobMatch]:
        try:
            # Get all active jobs
            jobs = await self.search_jobs(JobSearch())
            
            # Use OpenAI to calculate match scores
            matches = []
            for job in jobs:
                response = await openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "Calculate job match score and provide reasons based on resume and job description."
                        },
                        {
                            "role": "user",
                            "content": f"Resume: {resume.model_dump_json()}\nJob: {job.model_dump_json()}"
                        }
                    ]
                )
                
                # Parse response to get match score and reasons
                # This is a simplified version - you'd need to properly parse the response
                match_data = response.choices[0].message.content
                match_score = 0.85  # Replace with actual score calculation
                match_reasons = ["Skills match", "Experience level match"]  # Replace with actual reasons
                
                matches.append(JobMatch(
                    job=job,
                    match_score=match_score,
                    match_reasons=match_reasons
                ))
            
            # Sort by match score and return top matches
            matches.sort(key=lambda x: x.match_score, reverse=True)
            return matches[:limit]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error matching jobs: {str(e)}")

    async def get_job(self, job_id: str) -> Optional[Job]:
        try:
            job_data = await self.repository.get_document("jobs", job_id)
            if not job_data:
                return None
            return Job(**job_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving job: {str(e)}")
