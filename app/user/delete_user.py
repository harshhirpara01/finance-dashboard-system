import traceback
from datetime import datetime
from common.common_function import get_current_user
from common.responses import successResponse, errorResponse, HEM_INTERNAL_SERVER_ERROR
from shared.db import get_db
from . import Create_User
from .route import user
from sqlalchemy.orm import Session
from fastapi import Depends, status



@user.delete("/Delete-User/{user_id}")
def soft_delete_user(user_id: int, db: Session = Depends(get_db),
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

        user_data.is_deleted = True
        user_data.deleted_at = datetime.utcnow()

        db.commit()

        return successResponse(
            status.HTTP_200_OK,
            "User deleted successfully",
        )

    except Exception:
        traceback.print_exc()
        db.rollback()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )