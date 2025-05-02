import sys
import os
# Set the path to execute main.py for run pytest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base
from models.employee_model import Employees


SQLALCHEMY_TEST_DB_URI = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DB_URI, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

client = TestClient(app)

@pytest.fixture
def test_employee():
    employee = Employees(
        name="Test",
        email="test@test.com",
        department="Serive"
    )
    db = TestingSessionLocal()
    db.add(employee)
    db.commit()
    db.refresh(employee)
    yield employee
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM employees;"))
        connection.commit()