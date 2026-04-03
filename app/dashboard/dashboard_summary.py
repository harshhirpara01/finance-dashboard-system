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



@dashboard.get("/Dashboard-Summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:


        total_income = db.query(func.sum(FinancialRecord.amount)).filter(
            FinancialRecord.type == "income",
            FinancialRecord.is_deleted == False
        ).scalar() or 0

        total_expense = db.query(func.sum(FinancialRecord.amount)).filter(
            FinancialRecord.type == "expense",
            FinancialRecord.is_deleted == False
        ).scalar() or 0

        net_balance = total_income - total_expense
        data = {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance
        }
        return successResponse(
            status.HTTP_200_OK,
            "Dashboard summary fetched successfully",

            jsonable_encoder(data)
        )

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )