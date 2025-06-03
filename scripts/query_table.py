import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import CallData

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to query the call_data table
def query_call_data():
    db = SessionLocal()
    try:
        # Query all records from the call_data table
        call_data_records = db.query(CallData).all()
        
        # Print the results
        for record in call_data_records:
            print(f"ID: {record.id}, Call Date: {record.call_date}, Base Price: {record.base_price}, Final Price: {record.final_price}, Load Origin: {record.load_origin}, Call Outcome: {record.call_outcome}, Call Duration: {record.call_duration}, Is Negotiated: {record.is_negotiated}, Load Destination: {record.load_destination}, Carrier Sentiment: {record.carrier_sentiment}")
    finally:
        db.close()

if __name__ == '__main__':
    query_call_data() 