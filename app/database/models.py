from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.database.connection import Base

class CallData(Base):
    __tablename__ = 'call_data'

    id = Column(Integer, primary_key=True, index=True)
    call_date = Column(DateTime, nullable=True)
    base_price = Column(Float, nullable=True)
    final_price = Column(Float, nullable=True)
    load_origin = Column(String(100), nullable=True)
    call_outcome = Column(String(50), nullable=True)
    call_duration = Column(Integer, nullable=True)  # Duration in seconds
    is_negotiated = Column(Boolean, nullable=True)
    load_destination = Column(String(100), nullable=True)
    carrier_sentiment = Column(String(50), nullable=True) 