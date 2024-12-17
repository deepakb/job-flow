"""
Global exception handlers and custom exceptions for the application.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Any, Dict, Optional

class JobFlowException(Exception):
    """Base exception for all application-specific exceptions."""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class ResourceNotFoundException(JobFlowException):
    """Exception raised when a requested resource is not found."""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            message=f"{resource_type} with id {resource_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class AuthenticationException(JobFlowException):
    """Exception raised for authentication-related errors."""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class AuthorizationException(JobFlowException):
    """Exception raised when user doesn't have required permissions."""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )

class ValidationException(JobFlowException):
    """Exception raised for validation errors."""
    def __init__(self, message: str, errors: Dict[str, Any]):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"validation_errors": errors}
        )

class RateLimitException(JobFlowException):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, message: str, retry_after: int):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after": retry_after}
        )

async def jobflow_exception_handler(request: Request, exc: JobFlowException):
    """Handler for JobFlowException and its subclasses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
            "type": exc.__class__.__name__
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "details": {
                "validation_errors": exc.errors()
            },
            "type": "ValidationError"
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handler for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "type": "HTTPException"
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handler for unhandled exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "type": "InternalError"
        }
    )

def setup_exception_handlers(app):
    """Configure exception handlers for the FastAPI application."""
    app.add_exception_handler(JobFlowException, jobflow_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
