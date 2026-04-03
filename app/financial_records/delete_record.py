import traceback
from datetime import datetime

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


@records.delete("/Delete-Record/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:
        if current_user['role'] == "viewer":
            return errorResponse(
                status.HTTP_403_FORBIDDEN,
                "Access denied: Admins And Analyst only"
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

        record_data.is_deleted = True


        db.commit()

        data = {
            "id": record_id,
            "is_deleted": True
        }
        return successResponse(
            status.HTTP_200_OK,
            "Record deleted successfully",

            jsonable_encoder(data)
        )

    except Exception:
        traceback.print_exc()
        db.rollback()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )