import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Initialize the list of functions in session state
if 'functions' not in st.session_state:
    st.session_state['functions'] = []

# Function to add a new linear function
def add_function(label, intercept, slope):
    st.session_state['functions'].append({
        'Label': label,
        'Intercept (€)': intercept,  # Intercept = Initial value
        'Slope (€ per month)': slope  # Slope = Monthly increment
    })

# User interface to add a new function
st.title("Comparison of Linear Functions")
st.header("Add a new function")

label = st.text_input("Function label", value=f"Function {len(st.session_state['functions']) + 1}")
intercept = st.number_input("Intercept (€)", min_value=0.0, value=0.0, step=0.01)
slope = st.number_input("Slope (€ per month)", min_value=0.0, value=1000.0, step=0.01)

if st.button("Add function"):
    add_function(label, intercept, slope)

# Convert the function data into a DataFrame
df_functions = pd.DataFrame(st.session_state['functions'])

if not df_functions.empty:
    st.write("Functions added:")
    st.dataframe(df_functions)

    # Default dates for the simulation
    start_date = pd.to_datetime("2024-10-21")
    end_date = pd.to_datetime("2026-12-31")

    # Generate a time index with a daily step
    time_index = pd.date_range(start=start_date, end=end_date, freq='D')

    # Create a DataFrame to store the cumulative values for each function
    df_cumulative = pd.DataFrame(index=time_index)

    for i, function in df_functions.iterrows():
        # Intercept is applied at t=0 (start of the period)
        intercept_value = function['Intercept (€)']
        
        # Create a time series with the intercept applied at t=0
        cumulative_cost = pd.Series(intercept_value, index=time_index)

        # Apply the slope (monthly increment) continuously each month
        monthly_slope = pd.Series(function['Slope (€ per month)'], 
                                  index=pd.date_range(start=start_date, end=end_date, freq='MS'))

        # Reindex to match the daily time index, filling forward
        monthly_slope_daily = monthly_slope.reindex(time_index, method='ffill').fillna(0)

        # Apply the monthly increment continuously for each day, and keep the intercept at the start
        daily_increment = monthly_slope_daily / monthly_slope_daily.groupby(monthly_slope_daily.index.to_period('M')).transform('count')
        cumulative_cost += daily_increment.cumsum()

        # Add the function's cumulative cost to the DataFrame
        df_cumulative[function['Label']] = cumulative_cost

    # Plot the cumulative costs using Plotly
    fig = px.line(df_cumulative, x=df_cumulative.index, y=df_cumulative.columns, 
                  title="Comparison of Linear Functions")
    st.plotly_chart(fig)

else:
    st.write("No functions have been added yet.")
