import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Initialize the list of monthly cost profiles in session state
if 'cost_profiles' not in st.session_state:
    st.session_state['cost_profiles'] = []

# Function to add a new cost profile
def add_cost_profile(label, fixed_cost, monthly_cost):
    st.session_state['cost_profiles'].append({
        'Label': label,
        'Fixed Cost (€)': fixed_cost,  # Fixed cost = starting point (ordinate at the origin)
        'Monthly Cost (€)': monthly_cost  # Monthly cost = cost added every month
    })

# User interface to add a new cost profile
st.title("Comparison of Monthly Costs")
st.header("Add a new cost profile")

label = st.text_input("Cost profile label", value=f"Cost Profile {len(st.session_state['cost_profiles']) + 1}")
fixed_cost = st.number_input("Fixed Cost (€)", min_value=0.0, value=0.0, step=0.01)
monthly_cost = st.number_input("Monthly Cost (€)", min_value=0.0, value=1000.0, step=0.01)

if st.button("Add cost profile"):
    add_cost_profile(label, fixed_cost, monthly_cost)

# Convert the cost profile data into a DataFrame
df_cost_profiles = pd.DataFrame(st.session_state['cost_profiles'])

if not df_cost_profiles.empty:
    st.write("Cost profiles added:")
    st.dataframe(df_cost_profiles)

    # Default dates for the simulation
    start_date = pd.to_datetime("2024-10-21")
    end_date = pd.to_datetime("2026-12-31")

    # Generate a time index with a daily step
    time_index = pd.date_range(start=start_date, end=end_date, freq='D')

    # Create a DataFrame to store the cumulative costs for each profile
    df_cumulative = pd.DataFrame(index=time_index)

    for i, profile in df_cost_profiles.iterrows():
        # Fixed cost is applied at t=0 (start of the period)
        fixed_cost_value = profile['Fixed Cost (€)']
        
        # Create a time series with the fixed cost applied at t=0
        cumulative_cost = pd.Series(fixed_cost_value, index=time_index)

        # Apply the monthly cost at the start of each month (1st day of each month)
        monthly_cost_series = pd.Series(profile['Monthly Cost (€)'], 
                                        index=pd.date_range(start=start_date, end=end_date, freq='MS'))

        # Reindex to match the daily time index, filling forward
        monthly_cost_daily = monthly_cost_series.reindex(time_index, method='ffill').fillna(0)

        # Apply the monthly cost increase every 1st of the month, accumulating the cost each month
        cumulative_cost += monthly_cost_daily.cumsum()

        # Add the cost profile's cumulative cost to the DataFrame
        df_cumulative[profile['Label']] = cumulative_cost

    # Plot the cumulative costs using Plotly
    fig = px.line(df_cumulative, x=df_cumulative.index, y=df_cumulative.columns, 
                  title="Comparison of Monthly Costs")
    st.plotly_chart(fig)

else:
    st.write("No cost profiles have been added yet.")