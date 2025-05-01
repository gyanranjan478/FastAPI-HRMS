from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Path for the sqlite database
SQLALCHEMY_DATABASE_URL = 'sqlite:///./hrms.db'

# Create a connection engine to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Create an object of session maker to establish a new session for the database
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Create Base to track models and map them to database tables
Base = declarative_base()
