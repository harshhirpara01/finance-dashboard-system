import traceback

from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from shared.db import get_db
from common.responses import successResponse, errorResponse, HEM_INTERNAL_SERVER_ERROR
from common.common_function import get_current_user
from sqlalchemy import func
from app.user.models.create_user import Create_User
from .models.financial_record import FinancialRecord
from .route import records
from .schemas.financial_record_schema import CreateFinancialRecordSchema
from fastapi import Depends, status, Query
from typing import Optional
from datetime import date


@records.get("/Get-Record-By-ID/{record_id}")
def get_record_by_id(
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

        response_data = {
            "id": record_data.id,
            "amount": record_data.amount,
            "type": record_data.type,
            "category": record_data.category,
            "record_date": str(record_data.record_date),
            "notes": record_data.notes,
            "created_by": record_data.created_by
        }

        return successResponse(
            status.HTTP_200_OK,
            "Record fetched successfully",
            jsonable_encoder(response_data)
        )

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )