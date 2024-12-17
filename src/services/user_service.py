from typing import Optional
from models.user import UserCreate, UserUpdate, UserInDB
from repositories.firebase import FirebaseRepository
from fastapi import HTTPException

class UserService:
    def __init__(self):
        self.repository = FirebaseRepository()

    async def create_user(self, user_data: UserCreate) -> UserInDB:
        try:
            firebase_user = await self.repository.create_user(
                email=user_data.email,
                password=user_data.password,
                display_name=user_data.name
            )
            
            # Create additional user data in Firestore
            user_data_dict = user_data.model_dump(exclude={'password'})
            await self.repository.update_user(
                firebase_user['id'],
                user_data_dict
            )
            
            return UserInDB(
                id=firebase_user['id'],
                **user_data_dict
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user(self, user_id: str) -> Optional[UserInDB]:
        try:
            user_data = await self.repository.get_user(user_id)
            if not user_data:
                return None
            return UserInDB(**user_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserInDB]:
        try:
            # Get existing user
            existing_user = await self.get_user(user_id)
            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Update only provided fields
            update_data = user_data.model_dump(exclude_unset=True)
            await self.repository.update_user(user_id, update_data)
            
            # Get updated user
            updated_user = await self.get_user(user_id)
            return updated_user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def verify_token(self, token: str) -> dict:
        try:
            return await self.repository.verify_token(token)
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )
