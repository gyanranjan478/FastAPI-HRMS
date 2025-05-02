from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base
import uuid

'''
Create employee model
'''
class Employees(Base):
    __tablename__ = 'employees'

    id = Column(String, primary_key=True, index=True,  default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, unique=True, index=True)
    department = Column(String)

