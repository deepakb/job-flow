"""
Repository package for database operations.

This package provides repository implementations for different data models,
following the repository pattern for clean separation of data access logic.

Available Repositories:
- BaseRepository: Abstract base class for repositories
- UserRepository: User data management
- ResumeRepository: Resume data management
- JobRepository: Job data management
- ApplicationRepository: Job application management
"""

from .base import BaseRepository
from .user import UserRepository
from .resume import ResumeRepository
from .job import JobRepository
from .application import ApplicationRepository

__all__ = [
    'BaseRepository',
    'UserRepository',
    'ResumeRepository',
    'JobRepository',
    'ApplicationRepository'
]
