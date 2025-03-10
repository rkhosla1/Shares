import streamlit as st
import pandas as pd

# Function to calculate grant amounts
def calculate_grant_amounts(base_value, pbt_growth, years):
    grant_values = [base_value]
    for _ in range(1, years):
        new_value = grant_values[-1] * (1 + pbt_growth)
        grant_values.append(new_value)
    return grant_values

# Streamlit UI
st.title("📈 Share Buyback Calculator")

# Sidebar inputs
st.sidebar.header("🔢 Input Parameters")
redemption_pct = st.sidebar.slider("Redemption % (Max 100%)", 0, 100, 10) / 100
pbt_growth = st.sidebar.slider("Annual PBT Growth Rate (%)", 0, 50, 20) / 100
years = st.sidebar.slider("Projection Years", 1, 10, 5)

# Allow users to input their own base values
st.sidebar.header("📊 Base Grant Values")
base_values = {
    "Scenario 1": st.sidebar.number_input("Base Value (Scenario 1)", value=1000, min_value=1),
    "Scenario 2": st.sidebar.number_input("Base Value (Scenario 2)", value=800, min_value=1),
    "Scenario 3": st.sidebar.number_input("Base Value (Scenario 3)", value=1200, min_value=1),
}

# Generate results
results = {"Year": list(range(1, years + 1))}
for scenario, base_value in base_values.items():
    results[scenario] = calculate_grant_amounts(base_value, pbt_growth, years)

# Convert to DataFrame
df_results = pd.DataFrame(results)

# Display results
st.write("### 📊 Buyback Projection Table")
st.dataframe(df_results.style.format("{:,.2f}"))

# Plot results
st.line_chart(df_results.set_index("Year"))

# CSV Download Option
csv = df_results.to_csv(index=False).encode("utf-8")
st.download_button(label="📥 Download CSV", data=csv, file_name="buyback_projection.csv", mime="text/csv")
