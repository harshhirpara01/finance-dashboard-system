import hashlib
from datetime import datetime, timedelta, timezone
import uuid
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
import os
from dotenv import load_dotenv
from jose import JWTError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


from app.user.models.create_user import Create_User
from common.responses import errorResponse, successResponse
from shared.db import get_db

load_dotenv()

security = HTTPBearer()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    sha = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha, hashed_password)


JWT_SECRET =os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


def create_token(email, uid,role):
    try:
        uniq_key = uuid.uuid4().hex
        now = datetime.utcnow()
        expire = now + timedelta(minutes=5)
        token_details = {
            "email": email,
            "id": uid,
            "role":role,
            "iat": now,
            "exp": expire,
            "public_key": uniq_key,
            "login_type": 'WEB'
        }

        access_token = jwt.encode(token_details, JWT_SECRET, algorithm=ALGORITHM)
        return access_token

    except Exception as e:
        return {"code": 500, "status": "error", "message": f"Exception occurred while creating token: {e}"}



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])

        user_id = payload.get("id")
        email = payload.get("email")
        role = payload.get("role")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return {
            "id": user_id,
            "email": email,
            "role": role
        }

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired"
        )
def admin_required(current_user: Create_User = Depends(get_current_user)):
    if current_user.role != "admin":
        return errorResponse(
            status.HTTP_403_FORBIDDEN,
            "Only admin allowed"
        )
    return current_user
