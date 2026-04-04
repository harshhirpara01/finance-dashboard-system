import traceback
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from shared.db import get_db
from common.responses import successResponse, errorResponse, HEM_INTERNAL_SERVER_ERROR
from common.common_function import get_current_user
from app.user.models.create_user import Create_User
from app.financial_records.models.financial_record import FinancialRecord
from .route import dashboard
from sqlalchemy import func


@dashboard.get("/Recent-Activity")
def recent_activity(
    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:
        records = db.query(FinancialRecord).filter(
            FinancialRecord.is_deleted == False
        ).order_by(FinancialRecord.id.desc()).limit(5).all()

        data = []
        for rec in records:
            data.append({
                "id": rec.id,
                "amount": rec.amount,
                "type": rec.type,
                "category": rec.category,
                "date": str(rec.record_date)
            })

        return successResponse(
            status.HTTP_200_OK,
            "Recent activity fetched successfully",
            jsonable_encoder(data)
        )

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )