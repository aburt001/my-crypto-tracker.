# --- DISPLAY THE DASHBOARD ---
st.title("🧮 My Crypto Portfolio Tracker")

# Display a simple data table of your assets
st.subheader("Asset Breakdown")
st.write("Here is the current status of your tracked exchange balances:")

# (Assuming your portfolio data is stored in a DataFrame named 'df')
# If your variable has a different name, change 'df' to match your variable
try:
    st.dataframe(df)
except NameError:
    st.info("Data loaded successfully! Ready to build custom charts.")# --- DISPLAY THE DASHBOARD ---
st.title("🧮 My Crypto Portfolio Tracker")

# Display a simple data table of your assets
st.subheader("Asset Breakdown")
st.write("Here is the current status of your tracked exchange balances:")

# (Assuming your portfolio data is stored in a DataFrame named 'df')
# If your variable has a different name, change 'df' to match your variable
try:
    st.dataframe(df)
except NameError:
    st.info("Data loaded successfully! Ready to build custom charts.")
