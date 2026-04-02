from operator import index

from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.sql import func
from shared.db import Base



class Create_User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable = False)
    email = Column(String(120), unique = True, nullable = False, index = True)
    password_hash = Column(String(255), nullable = False)
    role = Column(String(20), nullable=False, default = "viewer")
    country = Column(String(100), nullable = True)
    is_active = Column(Boolean, default = True, nullable = False)
    is_blocked = Column(Boolean, default  = False, nullable = False)
    is_deleted = Column(Boolean, default = False, nullable = False)
    created_at = Column(DateTime(timezone= True), server_default = func.now())
    updated_at = Column(DateTime(timezone =True), server_default =func.now(), onupdate =func.now())
    deleted_at = Column(DateTime(timezone= True), nullable=True)