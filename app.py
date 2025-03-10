import streamlit as st
import pandas as pd

# Function to calculate projected option values
def calculate_grant_amounts(base_value, pbt_growth, redemption_pct, years):
    grant_values = [base_value]
    for _ in range(1, years):
        new_value = grant_values[-1] * (1 + pbt_growth) * (1 - redemption_pct)
        grant_values.append(new_value)
    return grant_values

# Streamlit UI
st.title("📈 Share Buyback & Growth Calculator")

# Sidebar for user inputs
st.sidebar.header("🔢 Input Parameters")

# Growth Rate Selection (15% - 20%)
pbt_growth = st.sidebar.slider("Annual Growth Rate (%)", 15, 20, 17) / 100

# Redemption Rate (0% - 10%)
redemption_pct = st.sidebar.slider("Annual Redemption Rate (%)", 0, 10, 5) / 100

# Total Granted Options
total_granted = st.sidebar.number_input("Total Granted Options", min_value=1, value=10000, step=100)

# Strike Price
strike_price = st.sidebar.number_input("Strike Price per Option ($)", min_value=0.01, value=50.0, step=0.1)

# Total Vested Options
total_vested = st.sidebar.number_input("Total Vested Options", min_value=1, value=8000, step=100)

# Projection Years
years = st.sidebar.slider("Projection Years", 1, 10, 5)

# Initial Grant Amount (Derived from Vested Options * Strike Price)
base_value = total_vested * strike_price

# Generate results
results = {"Year": list(range(1, years + 1))}
results["Projected Value"] = calculate_grant_amounts(base_value, pbt_growth, redemption_pct, years)

# Convert to DataFrame
df_results = pd.DataFrame(results)

# Display results
st.write("### 📊 Buyback & Growth Projection Table")
st.dataframe(df_results.style.format("${:,.2f}"))

# Plot results
st.line_chart(df_results.set_index("Year"))

# CSV Download Option
csv = df_results.to_csv(index=False).encode("utf-8")
st.download_button(label="📥 Download CSV", data=csv, file_name="buyback_projection.csv", mime="text/csv")
