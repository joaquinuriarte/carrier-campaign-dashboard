from app.database.connection import SessionLocal
from app.database.models import CallData
from datetime import datetime, timedelta
import pandas as pd

def get_call_data(start_date=None, end_date=None):
    """
    Get call data with optional date filtering
    """
    db = SessionLocal()
    try:
        query = db.query(CallData)
        
        if start_date and end_date:
            query = query.filter(
                CallData.call_date >= start_date,
                CallData.call_date <= end_date
            )
        
        records = query.all()
        
        # Convert to pandas DataFrame
        data = []
        for record in records:
            data.append({
                'ID': record.id,
                'Call Date': record.call_date,
                'Base Price': record.base_price,
                'Final Price': record.final_price,
                'Load Origin': record.load_origin,
                'Call Outcome': record.call_outcome,
                'Call Duration': record.call_duration,
                'Is Negotiated': record.is_negotiated,
                'Load Destination': record.load_destination,
                'Carrier Sentiment': record.carrier_sentiment
            })
        return pd.DataFrame(data)
    finally:
        db.close()

def get_summary_metrics():
    """
    Get summary metrics for the dashboard
    """
    df = get_call_data()
    if df.empty:
        return {
            'total_calls': 0,
            'avg_base_price': 0,
            'avg_final_price': 0,
            'negotiation_rate': 0
        }
    
    return {
        'total_calls': len(df),
        'avg_base_price': df['Base Price'].mean(),
        'avg_final_price': df['Final Price'].mean(),
        'negotiation_rate': (df['Is Negotiated'].sum() / len(df)) * 100
    } 