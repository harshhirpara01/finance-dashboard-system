import traceback
from common.common_function import get_current_user
from common.responses import successResponse, HSM_SUCCESS, errorResponse, HEM_INTERNAL_SERVER_ERROR
from shared.db import get_db
from . import Create_User
from .route import user
from sqlalchemy.orm import Session
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from .schemas.user_schema import UpdateUserSchema


@user.patch("/User_Update/{user_id}")
def update_user(user_id: int, payload: UpdateUserSchema, db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):
    try:

        if current_user["role"] != "admin":
            return errorResponse(
                status.HTTP_403_FORBIDDEN,
                "Access denied: Admins only"
            )

        user_data = db.query(Create_User).filter(
            Create_User.id == user_id,
            Create_User.is_deleted == False
        ).first()

        if not user_data:
            return errorResponse(
                status.HTTP_404_NOT_FOUND,
                "User not found"
            )

        if payload.email and payload.email != user_data.email:
            existing_user = db.query(Create_User).filter(
                Create_User.email == payload.email,
                Create_User.id != user_id,
                Create_User.is_deleted == False
            ).first()

            if existing_user:
                return errorResponse(
                    status.HTTP_400_BAD_REQUEST,
                    "User with this email already exists"
                )

        update_data = payload.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user_data, key, value)

        db.commit()
        db.refresh(user_data)

        response_data = {
            "id": user_data.id,
            **update_data
        }

        return successResponse(
            status.HTTP_200_OK,
            "User updated successfully",
            jsonable_encoder(response_data)
        )

    except Exception:
        traceback.print_exc()
        db.rollback()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )