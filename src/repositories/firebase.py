import firebase_admin
from firebase_admin import credentials, auth, firestore
from core.config import get_settings
from typing import Optional, Dict, Any

settings = get_settings()

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized
    pass

db = firestore.client()

class FirebaseRepository:
    @staticmethod
    async def create_user(email: str, password: str, display_name: str) -> Dict[str, Any]:
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            return {
                "id": user.uid,
                "email": user.email,
                "display_name": user.display_name
            }
        except auth.EmailAlreadyExistsError:
            raise ValueError("Email already exists")

    @staticmethod
    async def get_user(user_id: str) -> Optional[Dict[str, Any]]:
        try:
            user_ref = db.collection('users').document(user_id)
            user_doc = user_ref.get()
            if user_doc.exists:
                return user_doc.to_dict()
            return None
        except Exception as e:
            raise Exception(f"Error getting user: {str(e)}")

    @staticmethod
    async def update_user(user_id: str, data: Dict[str, Any]) -> bool:
        try:
            user_ref = db.collection('users').document(user_id)
            user_ref.update(data)
            return True
        except Exception as e:
            raise Exception(f"Error updating user: {str(e)}")

    @staticmethod
    async def verify_token(token: str) -> Dict[str, Any]:
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception:
            raise ValueError("Invalid token")
