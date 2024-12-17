"""
Authentication utilities for the Job Flow API.

This module provides functions for JWT token handling and user authentication, including:
- JWT token creation and validation
- Password hashing and verification
- User authentication middleware
- OAuth2 token handling

The module uses industry-standard security practices:
- JWT tokens with HS256 algorithm
- Secure password hashing with bcrypt
- OAuth2 bearer token authentication
- Automatic token expiration
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext

from core.config import settings

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    """
    Token response model.
    
    Attributes:
        access_token: JWT access token string
        token_type: Type of token (always "bearer")
    """
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """
    Token payload model.
    
    Attributes:
        user_id: ID of the authenticated user
        exp: Token expiration timestamp
    """
    user_id: str
    exp: Optional[datetime] = None

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.
    
    This function creates a new JWT token for a user with:
    - User ID embedded in the payload
    - Configurable expiration time
    - HS256 signing algorithm
    
    Args:
        user_id: ID of the user to create token for
        expires_delta: Optional custom expiration time. If not provided,
                      uses default from settings
        
    Returns:
        str: Encoded JWT token string
        
    Example:
        ```python
        token = create_access_token(
            user_id="user123",
            expires_delta=timedelta(hours=1)
        )
        ```
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "user_id": user_id,
        "exp": expire
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    This function:
    - Decodes the JWT token
    - Verifies the signature
    - Checks token expiration
    - Returns the decoded payload
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Dict[str, Any]: Decoded token payload containing user_id and exp
        
    Raises:
        HTTPException: If token is invalid, expired, or has invalid signature
        
    Example:
        ```python
        try:
            payload = decode_token(token)
            user_id = payload["user_id"]
        except HTTPException:
            # Handle invalid token
            pass
        ```
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Get the current user ID from the JWT token.
    
    This dependency function:
    - Extracts the JWT token from the request
    - Validates the token
    - Returns the user ID from the payload
    
    Use this as a FastAPI dependency to protect routes:
    ```python
    @router.get("/protected")
    async def protected_route(user_id: str = Depends(get_current_user_id)):
        return {"message": f"Hello user {user_id}"}
    ```
    
    Args:
        token: JWT token from request (injected by FastAPI)
        
    Returns:
        str: Current authenticated user's ID
        
    Raises:
        HTTPException: If token is invalid or user ID not found
    """
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Uses bcrypt to securely verify passwords:
    - Constant-time comparison
    - Protection against timing attacks
    - Automatic salt handling
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
        
    Example:
        ```python
        if verify_password(login_password, stored_hash):
            # Password is correct
            pass
        ```
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password securely using bcrypt.
    
    Features:
    - Automatic salt generation
    - Configurable work factor
    - Industry-standard algorithm
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Securely hashed password
        
    Example:
        ```python
        hash = get_password_hash("user_password")
        # Store hash in database
        ```
    """
    return pwd_context.hash(password)
