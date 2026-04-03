import json
import traceback

from common.common_function import admin_required, get_current_user
from common.responses import successResponse, HSM_SUCCESS, errorResponse, HEM_INTERNAL_SERVER_ERROR
from shared.db import get_db
from . import Create_User
from .route import user
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder


@user.get("/Get_Users_By_Id")
def get_user_by_id(user_id: int,db:Session = Depends(get_db),
                   current_user = Depends(get_current_user)
                   ):

    try:
        if current_user["role"] != "admin":
            return errorResponse(
                status.HTTP_403_FORBIDDEN,
                "Access denied: Admins only"
            )




        users = db.query(Create_User).filter(
            Create_User.id == user_id,
            Create_User.is_deleted == False
        ).first()

        if not users:
            return errorResponse(status.HTTP_404_NOT_FOUND,
                "User not found"
            )

        return  successResponse(status.HTTP_200_OK,
            "User fetched successfully",
            jsonable_encoder(users))

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )
    