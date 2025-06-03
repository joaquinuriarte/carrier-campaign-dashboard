from app.database.connection import SessionLocal
from app.database.models import CallData
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy.orm import Session
from app.database.connection import get_db

def get_call_data(start_date=None, end_date=None):
    """
    Retrieve call data from the database with optional date filtering
    """
    db = next(get_db())
    try:
        query = db.query(CallData)
        
        if start_date and end_date:
            query = query.filter(
                CallData.call_date >= start_date,
                CallData.call_date <= end_date
            )
        
        # Convert to DataFrame
        df = pd.read_sql(query.statement, query.session.bind)
        
        # Rename columns for display
        if not df.empty:
            df = df.rename(columns={
                'call_date': 'Call Date',
                'base_price': 'Base Price',
                'final_price': 'Final Price',
                'load_origin': 'Load Origin',
                'call_outcome': 'Call Outcome',
                'call_duration': 'Call Duration',
                'is_negotiated': 'Is Negotiated',
                'load_destination': 'Load Destination',
                'carrier_sentiment': 'Carrier Sentiment'
            })
        
        return df
    finally:
        db.close()

def get_calls_metrics():
    """
    Calculate calls-specific metrics including total calls and cumulative average duration
    """
    df = get_call_data()
    
    if df.empty:
        return {
            'total_calls': 0,
            'cumulative_avg_duration': pd.DataFrame()
        }
    
    # Filter for calls with non-null call_outcome
    valid_calls = df[df['Call Outcome'].notna()]
    
    # Calculate cumulative average duration
    if not valid_calls.empty:
        # Sort by date
        valid_calls = valid_calls.sort_values('Call Date')
        
        # Calculate cumulative average
        valid_calls['Cumulative Avg Duration'] = valid_calls['Call Duration'].expanding().mean()
        
        # Create time series data
        cumulative_avg = valid_calls[['Call Date', 'Cumulative Avg Duration']].copy()
    else:
        cumulative_avg = pd.DataFrame(columns=['Call Date', 'Cumulative Avg Duration'])
    
    return {
        'total_calls': len(valid_calls),
        'cumulative_avg_duration': cumulative_avg
    }

def get_outcome_metrics():
    """
    Calculate call outcome metrics and trends
    """
    df = get_call_data()
    
    if df.empty:
        return {
            'current_metrics': {
                'success_rate_booked': 0,
                'rate_too_low': 0,
                'no_matching_loads': 0,
                'ineligible_mc_number': 0
            },
            'trends': pd.DataFrame()
        }
    
    # Calculate current percentages
    current_metrics = {
        'success_rate_booked': (df['Call Outcome'] == 'success_rate_booked').mean(),
        'rate_too_low': (df['Call Outcome'] == 'rate_too_low').mean(),
        'no_matching_loads': (df['Call Outcome'] == 'no_matching_loads').mean(),
        'ineligible_mc_number': (df['Call Outcome'] == 'ineligible_mc_number').mean()
    }
    
    # Calculate daily trends
    df['date'] = pd.to_datetime(df['Call Date']).dt.date
    daily_outcomes = df.groupby('date')['Call Outcome'].value_counts(normalize=True).unstack(fill_value=0)
    
    # Ensure all outcome columns exist
    for outcome in ['success_rate_booked', 'rate_too_low', 'no_matching_loads', 'ineligible_mc_number']:
        if outcome not in daily_outcomes.columns:
            daily_outcomes[outcome] = 0
    
    # Reset index to make date a column
    daily_outcomes = daily_outcomes.reset_index()
    daily_outcomes['date'] = pd.to_datetime(daily_outcomes['date'])
    
    return {
        'current_metrics': current_metrics,
        'trends': daily_outcomes
    }

def get_negotiation_metrics():
    """
    Calculate negotiation metrics and price increase trends
    """
    df = get_call_data()
    
    if df.empty:
        return {
            'negotiation_rate': 0,
            'price_increase_trends': pd.DataFrame()
        }
    
    # Calculate overall negotiation rate
    valid_negotiations = df['Is Negotiated'].notna()
    negotiation_rate = (df.loc[valid_negotiations, 'Is Negotiated'].sum() / valid_negotiations.sum()) * 100
    
    # Calculate price increase trends
    df['date'] = pd.to_datetime(df['Call Date']).dt.date
    df['price_increase'] = ((df['Final Price'] - df['Base Price']) / df['Base Price']) * 100
    
    # Calculate daily average price increase
    daily_increases = df.groupby('date')['price_increase'].mean().reset_index()
    daily_increases['date'] = pd.to_datetime(daily_increases['date'])
    
    return {
        'negotiation_rate': negotiation_rate,
        'price_increase_trends': daily_increases
    }

def get_sentiment_metrics():
    """
    Calculate carrier sentiment metrics and trends
    """
    df = get_call_data()
    
    if df.empty:
        return {
            'trends': pd.DataFrame()
        }
    
    # Calculate daily sentiment distribution
    df['date'] = pd.to_datetime(df['Call Date']).dt.date
    daily_sentiments = df.groupby('date')['Carrier Sentiment'].value_counts(normalize=True).unstack(fill_value=0)
    
    # Ensure all sentiment columns exist
    for sentiment in ['carrier_sentiment_positive', 'carrier_sentiment_negative', 'carrier_sentiment_neutral']:
        if sentiment not in daily_sentiments.columns:
            daily_sentiments[sentiment] = 0
    
    # Reset index to make date a column
    daily_sentiments = daily_sentiments.reset_index()
    daily_sentiments['date'] = pd.to_datetime(daily_sentiments['date'])
    
    return {
        'trends': daily_sentiments
    } 