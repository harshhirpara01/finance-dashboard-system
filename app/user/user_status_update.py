
import traceback
from datetime import datetime
from common.common_function import get_current_user
from common.responses import successResponse, HSM_SUCCESS, errorResponse, HEM_INTERNAL_SERVER_ERROR
from shared.db import get_db
from . import Create_User
from .route import user
from sqlalchemy.orm import Session
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder

from .schemas.user_schema import StatusUserSchema


@user.patch("/User-Status-Update/{user_id}")
def update_user_status(
    user_id: int,
    payload: StatusUserSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
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

        user_data.is_active = payload.is_active
        db.commit()
        db.refresh(user_data)
        data = {
            "id": user_data.id,
            "is_active": user_data.is_active
        }
        return successResponse(
            status.HTTP_200_OK,
            "User status updated successfully",

            jsonable_encoder(data)
        )

    except Exception:
        traceback.print_exc()
        db.rollback()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )