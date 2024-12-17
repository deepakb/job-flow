"""
Notification API endpoints.

This module provides API endpoints for managing user notifications, including:
- Retrieving user notifications
- Marking notifications as read
- Managing notification preferences
- Real-time notification updates
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from models.notification import Notification, NotificationPreferences
from services.notification_service import NotificationService
from core.auth import get_current_user_id

router = APIRouter()

@router.get("/",
    response_model=List[Notification],
    summary="Get user notifications",
    description="""
    Retrieve notifications for the current user.
    
    Supports:
    * Filtering unread notifications
    * Pagination with offset and limit
    * Sorting by date (newest first)
    
    Notifications include:
    * Job application updates
    * Interview invitations
    * Resume match alerts
    * System announcements
    """,
    response_description="List of user notifications",
    responses={
        200: {
            "description": "Successfully retrieved notifications",
            "content": {
                "application/json": {
                    "example": [{
                        "id": "notif123",
                        "type": "application_update",
                        "title": "Application Status Update",
                        "message": "Your application for Senior Backend Engineer at Tech Corp has been reviewed",
                        "created_at": "2024-12-17T13:30:00Z",
                        "read": False
                    }]
                }
            }
        },
        401: {"description": "Invalid or expired token"}
    }
)
async def get_notifications(
    unread_only: Optional[bool] = False,
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of items to return"),
    user_id: str = Depends(get_current_user_id)
) -> List[Notification]:
    """
    Get notifications for the current user.
    
    Args:
        unread_only: If True, only return unread notifications
        offset: Number of items to skip for pagination
        limit: Maximum number of items to return
        user_id: ID of the authenticated user (from JWT token)
        
    Returns:
        List[Notification]: List of user notifications
        
    Raises:
        HTTPException: If authentication fails
    """
    service = NotificationService()
    notifications = await service.get_user_notifications(
        user_id,
        unread_only=unread_only,
        offset=offset,
        limit=limit
    )
    return [Notification(**notif.model_dump()) for notif in notifications]

@router.post("/{notification_id}/read",
    response_model=Notification,
    summary="Mark notification as read",
    description="""
    Mark a specific notification as read.
    
    This will:
    * Update the notification's read status
    * Update the user's unread count
    * Return the updated notification
    """,
    response_description="Updated notification",
    responses={
        200: {
            "description": "Successfully marked as read",
            "content": {
                "application/json": {
                    "example": {
                        "id": "notif123",
                        "type": "application_update",
                        "title": "Application Status Update",
                        "read": True,
                        "read_at": "2024-12-17T13:30:00Z"
                    }
                }
            }
        },
        401: {"description": "Invalid or expired token"},
        404: {"description": "Notification not found"}
    }
)
async def mark_as_read(
    notification_id: str,
    user_id: str = Depends(get_current_user_id)
) -> Notification:
    """
    Mark a notification as read.
    
    Args:
        notification_id: ID of the notification to mark as read
        user_id: ID of the authenticated user (from JWT token)
        
    Returns:
        Notification: Updated notification object
        
    Raises:
        HTTPException: If notification not found or not authorized
    """
    service = NotificationService()
    notification = await service.mark_as_read(notification_id, user_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return Notification(**notification.model_dump())

@router.post("/read-all",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Mark all notifications as read",
    description="""
    Mark all notifications as read for the current user.
    
    This will:
    * Update all unread notifications
    * Reset the user's unread count to 0
    * Clear any notification badges
    """,
    responses={
        204: {"description": "Successfully marked all as read"},
        401: {"description": "Invalid or expired token"}
    }
)
async def mark_all_read(user_id: str = Depends(get_current_user_id)):
    """
    Mark all notifications as read.
    
    Args:
        user_id: ID of the authenticated user (from JWT token)
        
    Raises:
        HTTPException: If authentication fails
    """
    service = NotificationService()
    await service.mark_all_as_read(user_id)

@router.get("/preferences",
    response_model=NotificationPreferences,
    summary="Get notification preferences",
    description="""
    Get the current user's notification preferences.
    
    Preferences include:
    * Email notification settings
    * Push notification settings
    * Notification frequency
    * Types of notifications enabled
    """,
    response_description="User's notification preferences",
    responses={
        200: {
            "description": "Successfully retrieved preferences",
            "content": {
                "application/json": {
                    "example": {
                        "email_enabled": True,
                        "push_enabled": True,
                        "frequency": "immediate",
                        "types": ["application_updates", "matches"]
                    }
                }
            }
        },
        401: {"description": "Invalid or expired token"}
    }
)
async def get_preferences(
    user_id: str = Depends(get_current_user_id)
) -> NotificationPreferences:
    """
    Get notification preferences.
    
    Args:
        user_id: ID of the authenticated user (from JWT token)
        
    Returns:
        NotificationPreferences: User's notification settings
        
    Raises:
        HTTPException: If preferences not found or authentication fails
    """
    service = NotificationService()
    prefs = await service.get_preferences(user_id)
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return NotificationPreferences(**prefs.model_dump())

@router.put("/preferences",
    response_model=NotificationPreferences,
    summary="Update notification preferences",
    description="""
    Update the current user's notification preferences.
    
    Configurable settings:
    * Email notifications (on/off)
    * Push notifications (on/off)
    * Notification frequency (immediate, daily, weekly)
    * Types of notifications to receive
    
    Changes take effect immediately for future notifications.
    """,
    response_description="Updated notification preferences",
    responses={
        200: {
            "description": "Successfully updated preferences",
            "content": {
                "application/json": {
                    "example": {
                        "email_enabled": True,
                        "push_enabled": False,
                        "frequency": "daily",
                        "types": ["application_updates"]
                    }
                }
            }
        },
        401: {"description": "Invalid or expired token"},
        422: {"description": "Invalid preference values"}
    }
)
async def update_preferences(
    preferences: NotificationPreferences,
    user_id: str = Depends(get_current_user_id)
) -> NotificationPreferences:
    """
    Update notification preferences.
    
    Args:
        preferences: New notification settings to apply
        user_id: ID of the authenticated user (from JWT token)
        
    Returns:
        NotificationPreferences: Updated notification settings
        
    Raises:
        HTTPException: If update fails or validation error occurs
    """
    service = NotificationService()
    updated_prefs = await service.update_preferences(user_id, preferences)
    return NotificationPreferences(**updated_prefs.model_dump())
