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
        'Intercept (€)': intercept,  # Intercept = Ordinate at the origin
        'Slope (€ per month)': slope  # Slope = Monthly increment
    })

# User interface to add a new function
st.title("Comparison of Cumulative Costs (Linear Functions)")
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

    # Create a DataFrame to store the cumulative costs for each function
    df_cumulative_costs = pd.DataFrame(index=time_index)

    for i, function in df_functions.iterrows():
        # Intercept is applied at t=0 (start of the period)
        intercept = function['Intercept (€)']
        
        # Slope is applied monthly, but the slope per day is slope / 30.44 (average days per month)
        daily_slope = function['Slope (€ per month)'] / 30.44
        
        # Create a linear function over time: intercept + slope * time
        cumulative_cost = intercept + np.arange(len(time_index)) * daily_slope

        # Add the function's cumulative cost to the DataFrame
        df_cumulative_costs[function['Label']] = cumulative_cost

    # Plot the cumulative costs using Plotly
    fig = px.line(df_cumulative_costs, x=df_cumulative_costs.index, y=df_cumulative_costs.columns, 
                  title="Comparison of Cumulative Costs (Linear Functions)")
    st.plotly_chart(fig)

else:
    st.write("No functions have been added yet.")