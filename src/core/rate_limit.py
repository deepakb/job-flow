"""
Rate limiting middleware for FastAPI.

This module provides rate limiting functionality to protect API endpoints
from abuse and ensure fair usage of resources.
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import time
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
import asyncio
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimiter:
    """Rate limiter implementation using token bucket algorithm."""
    
    def __init__(self):
        self.WINDOW_SIZE = 60  # 1 minute window
        self.requests: Dict[str, Dict[str, Tuple[int, float]]] = defaultdict(dict)
        self.locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        
        # Default rate limits (requests per minute)
        self.default_limits = {
            "default": 60,  # Default for all endpoints
            "resume": {  # Resource-intensive endpoints
                "parse": 10,
                "enhance": 5,
                "analyze": 5
            },
            "jobs": {  # Job-related endpoints
                "search": 30,
                "apply": 20
            },
            "auth": {  # Authentication endpoints
                "login": 10,
                "register": 5
            }
        }
    
    async def is_rate_limited(
        self,
        key: str,
        endpoint: str,
        limit: Optional[int] = None
    ) -> Tuple[bool, Dict[str, any]]:
        """Check if a request should be rate limited."""
        async with self.locks[key]:
            now = time.time()
            
            # Get or set the request count and window start
            if key not in self.requests or endpoint not in self.requests[key]:
                self.requests[key][endpoint] = (0, now)
            
            count, window_start = self.requests[key][endpoint]
            
            # Reset window if needed
            if now - window_start >= self.WINDOW_SIZE:
                count = 0
                window_start = now
            
            # Get the rate limit for this endpoint
            if limit is None:
                parts = endpoint.split("/")
                if len(parts) >= 2:
                    category = parts[1]
                    operation = parts[2] if len(parts) > 2 else None
                    
                    if category in self.default_limits and isinstance(self.default_limits[category], dict):
                        if operation in self.default_limits[category]:
                            limit = self.default_limits[category][operation]
                        else:
                            limit = self.default_limits["default"]
                    else:
                        limit = self.default_limits["default"]
                else:
                    limit = self.default_limits["default"]
            
            # Check if rate limit is exceeded
            is_limited = count >= limit
            
            if not is_limited:
                count += 1
                self.requests[key][endpoint] = (count, window_start)
            
            remaining = max(0, limit - count)
            reset_time = window_start + self.WINDOW_SIZE
            
            return is_limited, {
                "limit": limit,
                "remaining": remaining,
                "reset": int(reset_time),
                "window": self.WINDOW_SIZE
            }

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for applying rate limits to FastAPI endpoints."""
    
    def __init__(self, app):
        """Initialize the middleware."""
        super().__init__(app)
        self.rate_limiter = RateLimiter()
    
    async def dispatch(self, request: Request, call_next):
        """Process the request and apply rate limiting."""
        # Skip rate limiting for health check endpoint
        if request.url.path == "/health":
            return await call_next(request)
            
        # Get client identifier (IP address or API key)
        client_id = request.client.host
        
        # Check rate limit
        is_limited, info = await self.rate_limiter.is_rate_limited(
            key=client_id,
            endpoint=request.url.path
        )
        
        # Set rate limit headers
        headers = {
            "X-RateLimit-Limit": str(info["limit"]),
            "X-RateLimit-Remaining": str(info["remaining"]),
            "X-RateLimit-Reset": str(info["reset"])
        }
        
        if is_limited:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests",
                    "type": "rate_limit_exceeded",
                    "retry_after": info["reset"] - int(time.time())
                },
                headers=headers
            )
        
        # Process the request
        response = await call_next(request)
        
        # Add rate limit headers to response
        for key, value in headers.items():
            response.headers[key] = value
        
        return response
