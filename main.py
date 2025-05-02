from fastapi import FastAPI
from models.employee_model import Base
from database import engine
from routers.employees.employee import router as employee_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define CORS origins (for example, allow requests from your frontend domain)
origins = [
    "http://localhost:3000"
]

# Add the CORSMiddleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows these origins
    allow_credentials=True,  # Allows cookies (if needed)
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Create database tables and do model bindings
Base.metadata.create_all(bind=engine)


@app.get("/",tags=["Health Check"] )
def health_check():
    return {'status': 'healthy'}

app.include_router(employee_router,  prefix="/employees", tags=["Employee"])



