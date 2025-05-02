from conftest import *
from routers.employees.employee import get_db
from fastapi import status, Query
from typing import Optional

app.dependency_overrides[get_db] = override_get_db

def test_get_all_employees(test_employee):
    response = client.get("/employees/all")


    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"][0]["name"] == "Test"
    assert data["data"][0]["email"] == "test@test.com"
    assert data["data"][0]["department"] == "Serive"

def test_get_employee_by_id(test_employee):
    response = client.get("/find/{b939ae72-023b-4760-8efa-834676906718}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_employee(test_employee):
    response = client.post("/employees/add",
                           json={"name": "Test2",
                            "email":"test2@test.com",
                            "department":"Test2"})
    assert response.status_code == status.HTTP_201_CREATED

def test_update_employee(test_employee):
    response = client.put("/employees/update/{b939ae72-023b-4760-8efa-834676906718}",
                           json={"name": "Test2",
                                 "email": "test2@test.com",
                                 "department": "Test2"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_employee(test_employee):
    response = client.delete("/employees/delete/{b939ae72-023b-4760-8efa-834676906718}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
