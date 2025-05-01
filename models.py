from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base
import uuid

'''
Create employee model
'''
class Employees(Base):
    __tablename__ = 'employees'

    id = Column(String, primary_key=True, index=True,  default=lambda: str(uuid.uuid4()))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    designation = Column(String)
    phone_number = Column(String)
    salary = Column(Integer)
    created_at = Column(DateTime, default=func.now())
