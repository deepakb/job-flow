from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    """
    Base user model containing common attributes.
    
    Attributes:
        email: User's email address
        name: User's full name
        skills: List of user's professional skills
        preferences: Dictionary of user preferences (e.g., job type, location)
    """
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., description="User's full name")
    skills: List[str] = Field(
        default_factory=list,
        description="List of user's professional skills"
    )
    preferences: dict = Field(
        default_factory=dict,
        description="Dictionary of user preferences (e.g., job type, location)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "name": "John Doe",
                "skills": ["Python", "FastAPI", "React"],
                "preferences": {
                    "job_type": "Full-time",
                    "location": "Remote",
                    "salary_range": "100000-150000"
                }
            }
        }

class UserCreate(UserBase):
    """
    Model for creating a new user, extends UserBase with password.
    
    Attributes:
        password: User's password (will be hashed)
    """
    password: str = Field(
        ...,
        description="User's password (min length: 8 characters)",
        min_length=8
    )

class UserUpdate(BaseModel):
    """
    Model for updating user information.
    All fields are optional.
    """
    name: Optional[str] = Field(None, description="User's full name")
    skills: Optional[List[str]] = Field(None, description="List of user's professional skills")
    preferences: Optional[dict] = Field(None, description="Dictionary of user preferences")

class UserInDB(UserBase):
    """
    Internal user model with additional database fields.
    
    Attributes:
        id: Unique identifier for the user
        is_active: Whether the user account is active
        is_verified: Whether the user's email is verified
    """
    id: str = Field(..., description="Unique identifier for the user")
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active"
    )
    is_verified: bool = Field(
        default=False,
        description="Whether the user's email is verified"
    )

class UserResponse(UserBase):
    """
    Model for user responses in API endpoints.
    Includes all public user information.
    """
    id: str = Field(..., description="Unique identifier for the user")
    is_active: bool = Field(..., description="Whether the user account is active")
    is_verified: bool = Field(..., description="Whether the user's email is verified")

class Token(BaseModel):
    """
    Model for authentication tokens.
    
    Attributes:
        access_token: JWT access token
        token_type: Type of token (usually "bearer")
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(
        default="bearer",
        description="Type of token (usually 'bearer')"
    )

class TokenData(BaseModel):
    """
    Model for decoded token data.
    
    Attributes:
        user_id: ID of the user the token belongs to
    """
    user_id: str = Field(..., description="ID of the user the token belongs to")
