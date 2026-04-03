from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean
from sqlalchemy.sql import func
from shared.db import Base


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)
    category = Column(String(100), nullable=False)
    record_date = Column(Date, nullable=False)
    notes = Column(String(255), nullable=True)

    is_deleted = Column(Boolean, default=False, nullable=False)

    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
