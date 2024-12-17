from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import UserCreate, UserUpdate, UserResponse, Token
from services.user_service import UserService

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    service = UserService()
    user = await service.create_user(user_data)
    return UserResponse(**user.model_dump())

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    service = UserService()
    token_data = await service.verify_token(credentials.credentials)
    user = await service.get_user(token_data['uid'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.model_dump())

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    service = UserService()
    token_data = await service.verify_token(credentials.credentials)
    updated_user = await service.update_user(token_data['uid'], user_data)
    return UserResponse(**updated_user.model_dump())
