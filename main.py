from fastapi import FastAPI
from models.employee_model import Base
from database import engine
from routers.employees.employee import router as employee_router

app = FastAPI()

# Create database tables and do model bindings
Base.metadata.create_all(bind=engine)


@app.get("/",tags=["Health Check"] )
def health_check():
    return {'status': 'healthy'}

app.include_router(employee_router,  prefix="/employees", tags=["Employee"])



