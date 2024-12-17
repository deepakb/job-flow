import PyPDF2
import io
from typing import Optional
from fastapi import HTTPException
import openai
from models.resume import Resume, ResumeEnhancement
from core.config import get_settings
from repositories.firebase import FirebaseRepository

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY

class ResumeService:
    def __init__(self):
        self.repository = FirebaseRepository()

    async def parse_resume(self, file_content: bytes, file_name: str) -> str:
        try:
            # Parse PDF content
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            
            return text_content
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing resume: {str(e)}")

    async def extract_resume_data(self, text_content: str) -> dict:
        try:
            # Use OpenAI to extract structured data
            response = await openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Extract structured resume data from the following text. Include: personal info, skills, education, and experience."},
                    {"role": "user", "content": text_content}
                ]
            )
            
            # Parse the response and convert to resume format
            structured_data = response.choices[0].message.content
            # Process structured data into resume format
            # This is a simplified version - you'd need to parse the response properly
            return structured_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting resume data: {str(e)}")

    async def enhance_resume(self, resume_id: str) -> ResumeEnhancement:
        try:
            resume = await self.get_resume(resume_id)
            if not resume:
                raise HTTPException(status_code=404, detail="Resume not found")

            # Use OpenAI to generate enhancement suggestions
            response = await openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze this resume and provide enhancement suggestions for summary, skills, experience, and education."},
                    {"role": "user", "content": resume.model_dump_json()}
                ]
            )
            
            suggestions = response.choices[0].message.content
            # Process suggestions into enhancement format
            return ResumeEnhancement(
                summary_suggestions=["Improve summary clarity"],  # Replace with actual suggestions
                skill_suggestions=["Add relevant technical skills"],
                experience_suggestions=["Quantify achievements"],
                education_suggestions=["Add relevant coursework"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error enhancing resume: {str(e)}")

    async def store_resume(self, user_id: str, resume_data: dict) -> Resume:
        try:
            # Store resume in Firestore
            resume_dict = {
                "user_id": user_id,
                **resume_data
            }
            # Add to Firestore and get document ID
            doc_ref = await self.repository.create_document("resumes", resume_dict)
            return Resume(id=doc_ref.id, **resume_dict)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error storing resume: {str(e)}")

    async def get_resume(self, resume_id: str) -> Optional[Resume]:
        try:
            resume_data = await self.repository.get_document("resumes", resume_id)
            if not resume_data:
                return None
            return Resume(**resume_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving resume: {str(e)}")

    async def get_user_resumes(self, user_id: str) -> list[Resume]:
        try:
            resumes_data = await self.repository.query_documents(
                "resumes",
                [("user_id", "==", user_id)]
            )
            return [Resume(**resume_data) for resume_data in resumes_data]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving user resumes: {str(e)}")
