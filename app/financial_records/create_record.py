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
from .schemas.financial_record_schema import CreateFinancialRecordSchema


@records.post("/Create-Record")
def create_financial_record(
    payload: CreateFinancialRecordSchema,
    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:
        if current_user["role"] != "admin":
            return errorResponse(
                status.HTTP_403_FORBIDDEN,
                "Access denied: Admins only"
            )
        print(current_user)
        new_record = FinancialRecord(
            amount=payload.amount,
            type=payload.type,
            category=payload.category,
            record_date=payload.record_date,
            notes=payload.notes,
            created_by=current_user['id'],
            is_deleted=False

        )

        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        response_data = {
            "id": new_record.id,
            "amount": new_record.amount,
            "type": new_record.type,
            "category": new_record.category,
            "record_date": str(new_record.record_date),
            "notes": new_record.notes,
            "created_by": new_record.created_by
        }

        return successResponse(
            status.HTTP_200_OK,
            "Financial record created successfully",
            jsonable_encoder(response_data)
        )

    except Exception:
        traceback.print_exc()
        db.rollback()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )
