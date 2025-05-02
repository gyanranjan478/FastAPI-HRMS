from starlette.responses import JSONResponse
from uuid import UUID
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from starlette import status
from database import SessionLocal
from models.employee_model import Employees

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
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    department: str = Field(min_length=3, max_length=50)

'''
Get list of all employees.
'''
@router.get("/all", status_code=status.HTTP_200_OK)
async def read_all(
        db: db_dependency,
        name: Optional[str] = Query(None),
        department: Optional[str] = Query(None),
        page: int = Query(1, ge=1),
        limit: int = Query(5, ge=1)
):

    skip = (page - 1) * limit

    response = db.query(Employees)
    if name:
        response = response.filter(Employees.name.contains(name))
    if department:
        response = response.filter(Employees.department.contains(department))

    total = response.count()

    response = response.offset(skip).limit(limit).all()
    next_page = page + 1 if skip + limit < total else None
    previous_page = page - 1 if page > 1 else None

    if not response:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Employee not found",
                "data": None
            }
        )

    return {
        "success": True,
        "message": "Employees list",
        "limit": limit,
        "current_page": page,
        "next_page": next_page,
        "previous_page": previous_page,
        "total": total,
        "data": response
    }

'''
Get single employee based on id.
'''
@router.get("/find/{id}", status_code=status.HTTP_200_OK)
async def read_one(db: db_dependency,
                   id: UUID ):

    # find the employee from the database
    employee_model = db.query(Employees).filter(Employees.id == str(id)).first()

    if employee_model is not None:
        return {
            "success": True,
            "message": "Employee found",
            "data": employee_model
        }

    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Employee not found",
                "data": None
            }
        )


'''
Add new employee.
'''
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_employee(db: db_dependency,
                          employee_request: EmployeeRequest):

    # Parse employee object to model
    employee_model = Employees(**employee_request.model_dump())

    # update the database
    try:
        db.add(employee_model)
        db.commit()
        db.refresh(employee_model)
        return {
            "success": True,
            "message": "New employee created",
            "data": employee_model
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Employee already exists {e}",
            "data": None
        }

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
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Employee not found",
                "data": None
            }
        )
        # raise HTTPException(status_code=404, detail="Employee not found")

    # Update all the properties of employee from the request
    employee_model.name = employee.name
    employee_model.email = employee.email
    employee_model.department = employee.department

    # Update the database
    db.add(employee_model)
    db.commit()

    return {
        "success": True,
        "message": "Employee updated",
        "data": employee_model
    }


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(db: db_dependency,
                          id: UUID ):

    # Find if employee exists
    employee_model = db.query(Employees).filter(Employees.id == str(id)).first()

    # If not exist than raise error and return
    if employee_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Employee not found",
                "data": None
            }
        )
        # raise HTTPException(status_code=404, detail="Employee not found")

    # Delete employee from the database
    db.query(Employees).filter(Employees.id == str(id)).delete()
    db.commit()

    return {
        "success": True,
        "message": "Employee deleted",
        "data": employee_model
    }
    







