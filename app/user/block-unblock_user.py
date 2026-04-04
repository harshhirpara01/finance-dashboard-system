import traceback
from common.common_function import get_current_user
from common.responses import successResponse, errorResponse, HEM_INTERNAL_SERVER_ERROR
from shared.db import get_db
from . import Create_User
from .route import user
from sqlalchemy.orm import Session
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from .schemas.user_schema import BlockUserSchema


@user.patch("/User/Block-Unblock/{user_id}")
def block_unblock_user(user_id: int, payload: BlockUserSchema, db: Session = Depends(get_db),
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

        user_data.is_blocked = payload.is_blocked

        db.commit()
        db.refresh(user_data)

        message = "User blocked successfully" if payload.is_blocked else "User unblocked successfully"

        return successResponse(
            status.HTTP_200_OK,
            message,
            jsonable_encoder(user_data)
        )

    except Exception:
        traceback.print_exc()
        db.rollback()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )