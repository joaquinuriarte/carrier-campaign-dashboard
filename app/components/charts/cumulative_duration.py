import streamlit as st
import plotly.express as px

def render_cumulative_duration_chart(
    data,
    x_col='Call Date',
    y_col='Cumulative Avg Duration',
    title='Cumulative Average Call Duration Over Time',
    x_label='Date',
    y_label='Average Duration (seconds)'
):
    """
    Render a cumulative average duration chart
    
    Args:
        data (pd.DataFrame): DataFrame containing the data to plot
        x_col (str): Name of the column to use for x-axis
        y_col (str): Name of the column to use for y-axis
        title (str): Chart title
        x_label (str): Label for x-axis
        y_label (str): Label for y-axis
    """
    if data.empty:
        st.info("No duration data available")
        return
    
    fig = px.line(
        data,
        x=x_col,
        y=y_col,
        title=title
    )
    
    # Customize the chart appearance
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode='x unified',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True) 