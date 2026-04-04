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
from sqlalchemy import func, case




@dashboard.get("/Weekly-Trends")
def get_weekly_trends(
    db: Session = Depends(get_db),
    current_user: Create_User = Depends(get_current_user)
):
    try:
        results = db.query(
            func.strftime("%Y", FinancialRecord.record_date).label("year"),
            func.strftime("%W", FinancialRecord.record_date).label("week"),
            func.sum(
                case(
                    (FinancialRecord.type == "income", FinancialRecord.amount),
                    else_=0
                )
            ).label("total_income"),
            func.sum(
                case(
                    (FinancialRecord.type == "expense", FinancialRecord.amount),
                    else_=0
                )
            ).label("total_expense")
        ).filter(
            FinancialRecord.is_deleted == False
        ).group_by(
            func.strftime("%Y", FinancialRecord.record_date),
            func.strftime("%W", FinancialRecord.record_date)
        ).order_by(
            func.strftime("%Y", FinancialRecord.record_date),
            func.strftime("%W", FinancialRecord.record_date)
        ).all()

        if not results:
            return errorResponse(
                status.HTTP_404_NOT_FOUND,
                "No weekly trend data found"
            )

        response_data = []

        for row in results:
            income = float(row.total_income or 0)
            expense = float(row.total_expense or 0)
            net_balance = income - expense

            if net_balance > 0:
                trend_status = "profit"
            elif net_balance < 0:
                trend_status = "loss"
            else:
                trend_status = "neutral"

            response_data.append({
                "year": int(row.year),
                "week": int(row.week),
                "total_income": income,
                "total_expense": expense,
                "net_balance": net_balance,
                "trend_status": trend_status
            })

        return successResponse(
            status.HTTP_200_OK,
            "Weekly trends fetched successfully",
            jsonable_encoder(response_data)
        )

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )