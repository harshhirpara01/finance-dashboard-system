import traceback
from datetime import datetime

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



@dashboard.get("/Category-Summary")
def category_summary(
    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:
        results = db.query(
            FinancialRecord.category,
            func.sum(FinancialRecord.amount).label("total")
        ).filter(
            FinancialRecord.is_deleted == False
        ).group_by(FinancialRecord.category).all()

        data = []
        for category, total in results:
            data.append({
                "category": category,
                "total": total
            })

        return successResponse(
            status.HTTP_200_OK,
            "Category summary fetched successfully",
            jsonable_encoder(data)
        )

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )