import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models
Base = declarative_base()

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 