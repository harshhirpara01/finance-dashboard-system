import traceback
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from shared.db import get_db
from common.responses import successResponse, errorResponse, HEM_INTERNAL_SERVER_ERROR
from common.common_function import get_current_user
from app.user.models.create_user import Create_User
from .models.financial_record import FinancialRecord
from .route import records
from fastapi import Depends, status, Query

@records.get("/Get-AllRecords")
def get_records(

    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:
        print(current_user)
        if current_user['role'] == "viewer":
            return errorResponse(
                status.HTTP_403_FORBIDDEN,
                "Access denied: Admins And Analyst only"
            )

        records = db.query(FinancialRecord).filter(
            FinancialRecord.is_deleted == False
        ).order_by(FinancialRecord.id.desc()).all()

        if not records:
            return errorResponse(
                status.HTTP_404_NOT_FOUND,
                "Record not found"
            )

        response_data = []
        for rec in records:
            response_data.append({
                "id": rec.id,
                "amount": rec.amount,
                "type": rec.type,
                "category": rec.category,
                "record_date": str(rec.record_date),
                "notes": rec.notes,
                "created_by": rec.created_by
            })

        return successResponse(
            status.HTTP_200_OK,
            "Records fetched successfully",
            jsonable_encoder(response_data)
        )

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )
