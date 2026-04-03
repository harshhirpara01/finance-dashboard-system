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
from sqlalchemy import func, extract, case



@dashboard.get("/monthly-trends")
def get_monthly_trends(
    db: Session = Depends(get_db),
    # current_user: Create_User = Depends(get_current_user)
):
    try:
        results = db.query(
            extract("year", FinancialRecord.record_date).label("year"),
            extract("month", FinancialRecord.record_date).label("month"),
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
            extract("year", FinancialRecord.record_date),
            extract("month", FinancialRecord.record_date)
        ).order_by(
            extract("year", FinancialRecord.record_date),
            extract("month", FinancialRecord.record_date)
        ).all()

        if not results:
            return errorResponse(
                status.HTTP_404_NOT_FOUND,
                msg="No monthly trend data found"
            )

        response_data = []
        previous_income = None
        previous_expense = None

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

            income_trend = "N/A"
            expense_trend = "N/A"

            if previous_income is not None:
                if income > previous_income:
                    income_trend = "increased"
                elif income < previous_income:
                    income_trend = "decreased"
                else:
                    income_trend = "stable"

            if previous_expense is not None:
                if expense > previous_expense:
                    expense_trend = "increased"
                elif expense < previous_expense:
                    expense_trend = "decreased"
                else:
                    expense_trend = "stable"

            response_data.append({
                "year": int(row.year),
                "month": int(row.month),
                "total_income": income,
                "total_expense": expense,
                "net_balance": net_balance,
                "trend_status": trend_status,
                "income_trend_vs_previous_month": income_trend,
                "expense_trend_vs_previous_month": expense_trend
            })

            previous_income = income
            previous_expense = expense

        return successResponse(
            status.HTTP_200_OK,
            "Monthly trend analysis fetched successfully",
            jsonable_encoder(response_data)
        )

    except Exception:
        traceback.print_exc()
        return errorResponse(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            HEM_INTERNAL_SERVER_ERROR
        )