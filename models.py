from sqlalchemy.dialects.oracle import NUMBER

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    designation = Column(String)
    phone_number = Column(String)
    salary = Column(NUMBER)
    created_at = Column(DateTime, default=func.now())
