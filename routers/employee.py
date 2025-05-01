
from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from database import SessionLocal
from models import Employees

router = APIRouter()

''' 
Create database instance
'''
def get_db():
    # Create database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency injection for sql
db_dependency = Annotated[Session, Depends(get_db)]

class EmployeeRequest(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    is_active: bool = False
    designation: str = Field(min_length=3, max_length=50)
    phone_number: str = Field(min_length=10, max_length=10)
    salary: float = 0

'''
Get list of all employees.
'''
@router.get("/all", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Employees).filter(Employees.is_active).all()


'''
Get single employee based on id.
'''
@router.get("/find/{id}", status_code=status.HTTP_200_OK)
async def read_one(db: db_dependency,
                   id: UUID ):

    # find the employee from the database
    employee_model = db.query(Employees).filter(Employees.id == str(id)).first()

    if employee_model is not None:
        return employee_model

    raise HTTPException(status_code=404, detail="Employee not found")


'''
Add new employee.
'''
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_employee(db: db_dependency,
                          employee_request: EmployeeRequest):

    # Parse employee object to model
    employee_model = Employees(**employee_request.model_dump())

    # update the database
    db.add(employee_model)
    db.commit()

'''
Update new employee.
'''
@router.put("/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_employee(db: db_dependency,
                          employee: EmployeeRequest,
                          id: UUID ):

    # Get existing employee from the database
    employee_model = db.query(Employees).filter(Employees.id == str(id)).first()

    if employee_model is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Update all the properties of employee from the request
    employee_model.first_name = employee.first_name
    employee_model.last_name = employee.last_name
    employee_model.email = employee.email
    employee_model.is_active = employee.is_active
    employee_model.designation = employee.designation
    employee_model.phone_number = employee.phone_number
    employee_model.salary = employee.salary

    # Update the database
    db.add(employee_model)
    db.commit()


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(db: db_dependency,
                          id: UUID ):

    # Find if employee exists
    employee_model = db.query(Employees).filter(Employees.id == str(id)).first()

    # If not exist than raise error and return
    if employee_model is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Delete employee from the database
    db.query(Employees).filter(Employees.id == str(id)).delete()
    db.commit()
    







