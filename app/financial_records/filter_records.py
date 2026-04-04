import traceback
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from shared.db import get_db
from common.responses import successResponse, errorResponse, HEM_INTERNAL_SERVER_ERROR
from common.common_function import get_current_user
from sqlalchemy import func
from app.user.models.create_user import Create_User
from .models.financial_record import FinancialRecord
from .route import records
from fastapi import Depends, status, Query
from typing import Optional
from datetime import date

@records.get("/Filter_Records")
def get_records(
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:
        if current_user['role'] == "viewer":
            return errorResponse(
                status.HTTP_403_FORBIDDEN,
                "Access denied: Admins And Analyst only"
            )

        query = db.query(FinancialRecord).filter(
            FinancialRecord.is_deleted == False
        )

        if type:
            query = query.filter(func.lower(FinancialRecord.type) == type.lower())

        if category:
            query = query.filter(func.lower(FinancialRecord.category) == category.lower())

        if start_date and end_date:
            query = query.filter(
                FinancialRecord.record_date >= start_date,
                FinancialRecord.record_date <= end_date
            )

        elif start_date:
            query = query.filter(FinancialRecord.record_date >= start_date)

        elif end_date:
            query = query.filter(FinancialRecord.record_date <= end_date)

        records = query.order_by(FinancialRecord.id.desc()).all()
        print("records",records)

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