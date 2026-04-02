import traceback

from common.common_function import verify_password, create_token
from common.responses import successResponse, HSM_SUCCESS, errorResponse, HEM_INTERNAL_SERVER_ERROR
from shared.db import get_db
from . import Create_User
from .route import user
from sqlalchemy.orm import Session
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder

from .schemas.login_schema import LoginSchema


@user.post("/Login")
def login(payload:LoginSchema,db:Session = Depends(get_db)):
    try:
        user_data = db.query(Create_User).filter(
            Create_User.email == payload.email,
            Create_User.is_deleted == False
        ).first()

        if not user_data:
            return errorResponse(
                status.HTTP_404_NOT_FOUND,
                msg="User not found"
            )

        if user_data.is_blocked:
            return errorResponse(
                status.HTTP_403_FORBIDDEN,
                msg="User is blocked"
            )

        if not verify_password(payload.password, user_data.password_hash):
            return errorResponse(
                status.HTTP_401_UNAUTHORIZED,
                msg="Invalid password"
            )



        token  = create_token(email=user_data.email,uid=user_data.id,role=user_data.role)
        data = {
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "id": user_data.id,
                    "full_name": user_data.full_name,
                    "email": user_data.email,
                    "role": user_data.role
                }
            }

        return successResponse(
            status.HTTP_200_OK,
            "Login successful",
            jsonable_encoder(data))

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )