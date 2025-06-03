import streamlit as st
import plotly.express as px
from app.services.data_service import (
    get_call_data, get_calls_metrics, 
    get_outcome_metrics, get_negotiation_metrics, get_sentiment_metrics
)
from app.components.charts.cumulative_duration import render_cumulative_duration_chart
from app.components.charts.outcome_trends import render_outcome_trends_chart

# Page config
st.set_page_config(
    page_title="Carrier Campaign Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data 
df = get_call_data() # TODO: For demo purposes, we are fetching entire dataset. Ideally we would fetch a subset of the data.

# Header with title and date filter
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Carrier Campaign Dashboard")
with col2:
    if not df.empty and 'Call Date' in df.columns:
        min_date = df['Call Date'].min()
        max_date = df['Call Date'].max()
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed"
        )
        
        # Filter data based on date range
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = get_call_data(start_date, end_date)

# Get metrics
calls_metrics = get_calls_metrics()
outcome_metrics = get_outcome_metrics()
negotiation_metrics = get_negotiation_metrics()
sentiment_metrics = get_sentiment_metrics()

# Main content
if not df.empty:
    # ============================================================================
    # SECTION 1: CALL METRICS & DURATION
    # ============================================================================
    st.header("Calls")
    
    # Create two columns for the metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Calls", calls_metrics['total_calls'])
    
    with col2:
        if not calls_metrics['cumulative_avg_duration'].empty:
            latest_avg = calls_metrics['cumulative_avg_duration']['Cumulative Avg Duration'].iloc[-1]
            st.metric("Average Call Duration", f"{latest_avg:.1f} seconds")
    
    # Render cumulative duration chart using the component
    render_cumulative_duration_chart(
        calls_metrics['cumulative_avg_duration'],
        x_col='Call Date',
        y_col='Cumulative Avg Duration',
        title='Cumulative Average Call Duration Over Time',
        x_label='Date',
        y_label='Average Duration (seconds)'
    )

    # ============================================================================
    # SECTION 2: CALL OUTCOMES & TRENDS
    # ============================================================================
    st.header("Call Outcomes")
    
    # First row: Current metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Successful Calls",
            f"{outcome_metrics['current_metrics']['success_rate_booked']:.1%}"
        )
    
    with col2:
        st.metric(
            "Rate Too Low",
            f"{outcome_metrics['current_metrics']['rate_too_low']:.1%}"
        )
    
    with col3:
        st.metric(
            "No Matching Loads",
            f"{outcome_metrics['current_metrics']['no_matching_loads']:.1%}"
        )
    
    with col4:
        st.metric(
            "Ineligible Driver",
            f"{outcome_metrics['current_metrics']['ineligible_mc_number']:.1%}"
        )
    
    # Second row: Trends chart
    render_outcome_trends_chart(
        outcome_metrics['trends'],
        date_col='date',
        y_columns=['success_rate_booked', 'rate_too_low', 'no_matching_loads', 'ineligible_mc_number'],
        y_labels={
            'success_rate_booked': 'Success Rate Booked',
            'rate_too_low': 'Rate Too Low',
            'no_matching_loads': 'No Matching Loads',
            'ineligible_mc_number': 'Ineligible Driver'
        },
        title='Call Outcome Trends Over Time',
        x_label='Date',
        y_label='Percentage'
    )

    # ============================================================================
    # SECTION 3: NEGOTIATION & SENTIMENT ANALYSIS
    # ============================================================================
    st.header("Negotiation & Sentiment")
    
    # First row: Negotiation rate
    st.metric(
        "Negotiated Calls",
        f"{negotiation_metrics['negotiation_rate']:.1f}%"
    )
    
    # Second row: Price increase trend
    if not negotiation_metrics['price_increase_trends'].empty:
        fig = px.line(
            negotiation_metrics['price_increase_trends'],
            x='date',
            y='price_increase',
            title='Average Price Increase Over Time',
            labels={
                'date': 'Date',
                'price_increase': 'Price Increase (%)'
            }
        )
        fig.update_layout(
            yaxis_title='Price Increase (%)',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Third row: Sentiment trends
    render_outcome_trends_chart(
        sentiment_metrics['trends'],
        y_columns=['carrier_sentiment_positive', 'carrier_sentiment_negative', 'carrier_sentiment_neutral'],
        y_labels={
            'carrier_sentiment_positive': 'Positive',
            'carrier_sentiment_negative': 'Negative',
            'carrier_sentiment_neutral': 'Neutral'
        },
        title='Carrier Sentiment Trends Over Time'
    )
else:
    st.info("No data available. Start by ingesting some call data through the API.") 