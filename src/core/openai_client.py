from openai import OpenAI
from core.config import get_settings
import time
from fastapi import HTTPException

settings = get_settings()

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.max_retries = 3
        self.retry_delay = 60  # seconds

    async def create_chat_completion(self, messages, model="gpt-4"):
        for attempt in range(self.max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                return response
            except Exception as e:
                if "rate limit" in str(e).lower():
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                raise HTTPException(
                    status_code=429,
                    detail="OpenAI rate limit reached. Please try again later."
                )
            
    async def create_embedding(self, text, model="text-embedding-ada-002"):
        for attempt in range(self.max_retries):
            try:
                response = await self.client.embeddings.create(
                    model=model,
                    input=text
                )
                return response
            except Exception as e:
                if "rate limit" in str(e).lower():
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                raise HTTPException(
                    status_code=429,
                    detail="OpenAI rate limit reached. Please try again later."
                )
