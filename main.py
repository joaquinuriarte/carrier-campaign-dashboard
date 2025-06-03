import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from app.services.data_service import get_call_data, get_summary_metrics

# Page config
st.set_page_config(
    page_title="Carrier Campaign Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("Carrier Campaign Dashboard")

# Load data
df = get_call_data()

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
if not df.empty and 'Call Date' in df.columns:
    min_date = df['Call Date'].min()
    max_date = df['Call Date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data based on date range
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = get_call_data(start_date, end_date)

# Get summary metrics
metrics = get_summary_metrics()

# Main content
if not df.empty:
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Calls", metrics['total_calls'])
    with col2:
        st.metric("Average Base Price", f"${metrics['avg_base_price']:.2f}")
    with col3:
        st.metric("Average Final Price", f"${metrics['avg_final_price']:.2f}")
    with col4:
        st.metric("Negotiation Rate", f"{metrics['negotiation_rate']:.1f}%")

    # Price distribution chart
    st.subheader("Price Distribution")
    fig = px.histogram(df, x=['Base Price', 'Final Price'],
                      title="Distribution of Base and Final Prices",
                      labels={'value': 'Price', 'variable': 'Price Type'})
    st.plotly_chart(fig, use_container_width=True)

    # Call outcomes
    st.subheader("Call Outcomes")
    outcome_counts = df['Call Outcome'].value_counts()
    fig = px.pie(values=outcome_counts.values, 
                 names=outcome_counts.index,
                 title="Distribution of Call Outcomes")
    st.plotly_chart(fig, use_container_width=True)

    # Raw data table
    st.subheader("Raw Data")
    st.dataframe(df)
else:
    st.info("No data available. Start by ingesting some call data through the API.") 