"""
OpenAI API client for AI-powered features.

This module provides a wrapper around the OpenAI API client with:
- Rate limiting and retry logic
- Error handling
- Response parsing
- Token usage tracking
"""

import openai
import backoff
import logging
from typing import List, Dict, Any, Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from core.config import settings

logger = logging.getLogger(__name__)

class OpenAIClient:
    """
    Client for interacting with OpenAI's API.
    
    Features:
    - Automatic retry with exponential backoff
    - Rate limit handling
    - Error logging and handling
    - Response validation
    
    Attributes:
        api_key: OpenAI API key
        model: GPT model to use
        max_retries: Maximum number of retry attempts
        timeout: Request timeout in seconds
    """
    
    def __init__(
        self,
        api_key: str = settings.OPENAI_API_KEY,
        model: str = "gpt-4",
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key
            model: GPT model to use (default: gpt-4)
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout
        openai.api_key = api_key

    @retry(
        retry=retry_if_exception_type((openai.error.RateLimitError, openai.error.APIError)),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3)
    )
    async def create_chat_completion(self, messages, model="gpt-4"):
        """
        Create a chat completion using AI.
        
        Args:
            messages: List of messages to use for completion
            model: GPT model to use (default: gpt-4)
            
        Returns:
            Response from OpenAI API
            
        Raises:
            OpenAIError: If API call fails after retries
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=messages
            )
            return response
            
        except Exception as e:
            logger.error(f"Error creating chat completion: {str(e)}")
            raise

    @retry(
        retry=retry_if_exception_type((openai.error.RateLimitError, openai.error.APIError)),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3)
    )
    async def create_embedding(self, text, model="text-embedding-ada-002"):
        """
        Create an embedding using AI.
        
        Args:
            text: Text to use for embedding
            model: Model to use for embedding (default: text-embedding-ada-002)
            
        Returns:
            Response from OpenAI API
            
        Raises:
            OpenAIError: If API call fails after retries
        """
        try:
            response = await openai.Embedding.acreate(
                model=model,
                input=text
            )
            return response
            
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            raise
