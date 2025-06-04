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
    Calculate call outcome metrics and daily counts
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
    
    # Calculate daily counts
    # First convert to datetime, handling NaT values
    df['date'] = pd.to_datetime(df['Call Date'], errors='coerce')
    # Drop rows with NaT dates
    df = df.dropna(subset=['date'])
    # Convert to date
    df['date'] = df['date'].dt.date
    
    if df.empty:
        return {
            'current_metrics': current_metrics,
            'trends': pd.DataFrame(columns=['date'])
        }
    
    # Create a complete date range
    min_date = df['date'].min()
    max_date = df['date'].max()
    date_range = pd.date_range(
        start=min_date,
        end=max_date,
        freq='D'
    )
    
    # Initialize the trends DataFrame with the complete date range
    daily_counts = pd.DataFrame({'date': date_range.date})
    
    # Calculate daily counts for each outcome
    for outcome in ['success_rate_booked', 'rate_too_low', 'no_matching_loads', 'ineligible_mc_number']:
        # Get daily counts for this outcome
        outcome_counts = df[df['Call Outcome'] == outcome].groupby('date').size()
        # Merge with the complete date range
        daily_counts = daily_counts.merge(
            outcome_counts.reset_index(name=outcome),
            on='date',
            how='left'
        )
    
    # Fill any missing values with 0
    daily_counts = daily_counts.fillna(0)
    
    return {
        'current_metrics': current_metrics,
        'trends': daily_counts
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
    Calculate carrier sentiment metrics and daily counts
    """
    df = get_call_data()
    
    if df.empty:
        return {
            'trends': pd.DataFrame()
        }
    
    # Calculate daily counts
    # First convert to datetime, handling NaT values
    df['date'] = pd.to_datetime(df['Call Date'], errors='coerce')
    # Drop rows with NaT dates
    df = df.dropna(subset=['date'])
    # Convert to date
    df['date'] = df['date'].dt.date
    
    if df.empty:
        return {
            'trends': pd.DataFrame(columns=['date'])
        }
    
    # Create a complete date range
    min_date = df['date'].min()
    max_date = df['date'].max()
    date_range = pd.date_range(
        start=min_date,
        end=max_date,
        freq='D'
    )
    
    # Initialize the trends DataFrame with the complete date range
    daily_counts = pd.DataFrame({'date': date_range.date})
    
    # Calculate daily counts for each sentiment
    for sentiment in ['carrier_sentiment_positive', 'carrier_sentiment_negative', 'carrier_sentiment_neutral']:
        # Get daily counts for this sentiment
        sentiment_counts = df[df['Carrier Sentiment'] == sentiment].groupby('date').size()
        # Merge with the complete date range
        daily_counts = daily_counts.merge(
            sentiment_counts.reset_index(name=sentiment),
            on='date',
            how='left'
        )
    
    # Fill any missing values with 0
    daily_counts = daily_counts.fillna(0)
    
    return {
        'trends': daily_counts
    } 