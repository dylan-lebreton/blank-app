import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Initialize the list of cost profiles in session state
if 'cost_profiles' not in st.session_state:
    st.session_state['cost_profiles'] = []

# Function to add a new cost profile
def add_cost_profile(label, fixed_cost, monthly_cost):
    st.session_state['cost_profiles'].append({
        'Label': label,
        'Fixed Cost (€)': fixed_cost,  # Fixed cost = Ordinate at the origin
        'Monthly Cost (€)': monthly_cost  # Monthly cost = Added every 1st of the month
    })

# Sidebar inputs for cost profiles
with st.sidebar:
    st.header("Add a new cost profile")
    label = st.text_input("Cost profile label", value=f"Cost Profile {len(st.session_state['cost_profiles']) + 1}")
    fixed_cost = st.number_input("Fixed Cost (€)", min_value=0.0, value=0.0, step=0.01)
    monthly_cost = st.number_input("Monthly Cost (€)", min_value=0.0, value=1000.0, step=0.01)

    # Default dates for the simulation
    start_date = st.date_input("Start Date", value=pd.to_datetime("2024-10-21"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2026-12-31"))

    if st.button("Add cost profile"):
        add_cost_profile(label, fixed_cost, monthly_cost)

# Convert the cost profile data into a DataFrame
df_cost_profiles = pd.DataFrame(st.session_state['cost_profiles'])

# Tabs for Profiles and Graph
tab1, tab2 = st.tabs(["Graph", "Profiles"])

with tab1:
    # Default tab is the graph
    if not df_cost_profiles.empty:
        # Generate a time index with a daily step
        time_index = pd.date_range(start=start_date, end=end_date, freq='D')

        # Create a DataFrame to store the cumulative costs for each profile
        df_cumulative = pd.DataFrame(index=time_index)

        for i, profile in df_cost_profiles.iterrows():
            # Fixed cost applied at the start
            fixed_cost_value = profile['Fixed Cost (€)']

            # Initialize the cumulative cost with fixed cost
            cumulative_cost = pd.Series(fixed_cost_value, index=time_index)

            # Apply the monthly cost at the start of each month
            monthly_cost = profile['Monthly Cost (€)']
            for date in pd.date_range(start=start_date, end=end_date, freq='MS'):
                if date == start_date and date.day == 1:
                    # If the graph starts on the 1st of the month, apply fixed + monthly cost at t=0
                    cumulative_cost[date:] += fixed_cost_value + monthly_cost
                else:
                    cumulative_cost[date:] += monthly_cost

            # Add the profile's cumulative cost to the DataFrame
            df_cumulative[profile['Label']] = cumulative_cost

        # Plot the cumulative costs using Plotly
        fig = px.line(df_cumulative, x=df_cumulative.index, y=df_cumulative.columns, 
                      title="Comparison of Monthly Costs")
        st.plotly_chart(fig)

    else:
        st.write("No cost profiles have been added yet.")

with tab2:
    # Display the profiles DataFrame in the "Profiles" tab
    st.write("Cost profiles added:")
    st.dataframe(df_cost_profiles)