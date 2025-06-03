import streamlit as st
import plotly.express as px

def render_outcome_trends_chart(
    data,
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
):
    """
    Render a normalized stacked area chart showing call outcome trends
    
    Args:
        data (pd.DataFrame): DataFrame containing the outcome trends data
        date_col (str): Name of the date column
        y_columns (list): List of column names to plot on y-axis
        y_labels (dict): Dictionary mapping column names to display labels
        title (str): Chart title
        x_label (str): Label for x-axis
        y_label (str): Label for y-axis
    """
    if data.empty:
        st.info("No outcome data available")
        return
    
    fig = px.area(
        data,
        x=date_col,
        y=y_columns,
        title=title,
        labels=y_labels
    )
    
    # Customize the chart appearance
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode='x unified',
        yaxis=dict(
            tickformat='.0%',
            range=[0, 1]
        )
    )
    
    st.plotly_chart(fig, use_container_width=True) 