from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional


class CreateUserSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    role: Literal["viewer", "analyst", "admin"] = "viewer"
    country: Optional[str] = None
    is_active: bool = True
    is_blocked: bool = False


class UserResponseSchema(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    country: Optional[str]
    is_active: bool
    is_blocked: bool
    is_deleted: bool

    class Config:
        from_attributes = True


class UpdateUserSchema(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[Literal["viewer", "analyst", "admin"]] = None
    country: Optional[str] = None


class BlockUserSchema(BaseModel):
    is_blocked: bool


class StatusUserSchema(BaseModel):
    is_active: bool
