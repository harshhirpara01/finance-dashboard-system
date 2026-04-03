from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date


class CreateFinancialRecordSchema(BaseModel):
    amount: float = Field(..., gt=0)
    type: Literal["income", "expense"]
    category: str = Field(..., min_length=2, max_length=100)
    record_date: date
    notes: Optional[str] = Field(None, max_length=255)
    
class UpdateFinancialRecordSchema(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    notes: Optional[str] = Field(None, max_length=255)