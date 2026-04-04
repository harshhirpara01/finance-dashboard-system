import traceback
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from shared.db import get_db
from common.responses import successResponse, errorResponse, HEM_INTERNAL_SERVER_ERROR
from common.common_function import get_current_user
from app.user.models.create_user import Create_User
from .models.financial_record import FinancialRecord
from .route import records
from .schemas.financial_record_schema import  UpdateFinancialRecordSchema


@records.patch("/Update-Record/{record_id}")
def update_record(
    record_id: int,
    payload: UpdateFinancialRecordSchema,
    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:
        if current_user['role'] != "admin":
            return errorResponse(
                status.HTTP_403_FORBIDDEN,
                "Access denied: Admins only"
            )

        record_data = db.query(FinancialRecord).filter(
            FinancialRecord.id == record_id,
            FinancialRecord.is_deleted == False
        ).first()

        if not record_data:
            return errorResponse(
                status.HTTP_404_NOT_FOUND,
                "Record not found"
            )

        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            return errorResponse(
                status.HTTP_400_BAD_REQUEST,
                "No fields provided for update"
            )

        for key, value in update_data.items():
            setattr(record_data, key, value)

        db.commit()
        db.refresh(record_data)

        response_data = {
            "id": record_data.id,
            **update_data
        }

        return successResponse(
            status.HTTP_200_OK,
            "Record updated successfully",
            jsonable_encoder(response_data)
        )

    except Exception:
        traceback.print_exc()
        db.rollback()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )