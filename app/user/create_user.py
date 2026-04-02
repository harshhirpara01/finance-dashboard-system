import traceback
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.user.models.create_user import Create_User
from shared.db import get_db
from common.responses import *
from .route import user
from app.user.schemas.user_schema import CreateUserSchema
import hashlib
from common.common_function import hash_password, admin_required


@user.post("/Create-User")
def create_user(payload : CreateUserSchema,db:Session = Depends(get_db),
                Current_user: Create_User = Depends(admin_required)
):
    try:

        existing_user = db.query(Create_User).filter(
            Create_User.email == payload.email,
            Create_User.is_deleted == False


        ).first()

        if existing_user:
            return errorResponse(status.HTTP_400_BAD_REQUEST,msg="User with this email already exists")

        # hashed_password = pwd_context.hash(payload.password)

        hashed_password = hash_password(payload.password)

        new_user = Create_User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=hashed_password,
            role=payload.role,
            country=payload.country,
            is_active=payload.is_active,
            is_blocked=payload.is_blocked,
            is_deleted=False
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return successResponse(status.HTTP_200_OK, HSM_SUCCESS,jsonable_encoder(new_user))

    except Exception as e:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )
