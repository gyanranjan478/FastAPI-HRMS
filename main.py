from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from models import Base
from database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {'status': 'healthy'}




