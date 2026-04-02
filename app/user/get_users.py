import traceback

from common.responses import successResponse, HSM_SUCCESS, errorResponse, HEM_INTERNAL_SERVER_ERROR
from shared.db import get_db
from . import Create_User
from .route import user
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder


@user.get("/Get-Users")
def get_users(db:Session = Depends(get_db)):
    try:
        users = db.query(Create_User).filter(
            Create_User.is_deleted == False
        ).all()

        return successResponse(status.HTTP_200_OK,HSM_SUCCESS,jsonable_encoder(users))

    except Exception as e:

        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )
