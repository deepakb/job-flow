"""
Application API endpoints.

This module provides API endpoints for managing job applications.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from models.job import JobApplication, ApplicationStatus, ApplicationUpdate
from services.application_service import ApplicationService
from core.auth import get_current_user_id

router = APIRouter()

@router.get("/",
    response_model=List[JobApplication],
    summary="Get user's applications"
)
async def get_applications(
    status: Optional[ApplicationStatus] = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: str = Depends(get_current_user_id)
) -> List[JobApplication]:
    """Get all applications for the current user."""
    service = ApplicationService()
    applications = await service.get_user_applications(
        user_id,
        status=status,
        offset=offset,
        limit=limit
    )
    return [JobApplication(**app.model_dump()) for app in applications]

@router.get("/{application_id}",
    response_model=JobApplication,
    summary="Get application details"
)
async def get_application(
    application_id: str,
    user_id: str = Depends(get_current_user_id)
) -> JobApplication:
    """Get detailed information about a specific application."""
    service = ApplicationService()
    application = await service.get_application(application_id, user_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return JobApplication(**application.model_dump())

@router.patch("/{application_id}",
    response_model=JobApplication,
    summary="Update application status"
)
async def update_application(
    application_id: str,
    update_data: ApplicationUpdate,
    user_id: str = Depends(get_current_user_id)
) -> JobApplication:
    """Update an application's status and details."""
    service = ApplicationService()
    updated_app = await service.update_application(
        application_id,
        user_id,
        update_data
    )
    return JobApplication(**updated_app.model_dump())

@router.delete("/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Withdraw application"
)
async def withdraw_application(
    application_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Withdraw a job application."""
    service = ApplicationService()
    await service.withdraw_application(application_id, user_id)
