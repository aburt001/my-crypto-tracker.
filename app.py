import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Set up page styling configuration
st.set_page_config(page_title="Crypto Portfolio Tracker", page_icon="🧮", layout="wide")

# --- TITLE & HEADERS ---
st.title("🧮 My Crypto Portfolio Tracker")
st.markdown("---")

# --- ACTUAL EXCHANGE PORTFOLIO DATA ---
# Update the balances below with your current token counts
# --- ACTUAL EXCHANGE PORTFOLIO DATA ---
df = pd.DataFrame({
    'Exchange': ['Kraken', 'Crypto.com', 'Kraken', 'Crypto.com', 'Kraken', 'Crypto.com'],
    'Asset': ['BTC', 'ETH', 'XLM', 'OSMO', 'LIT', 'ASRR'],
    'Balance': [0.45, 3.20, 12500.0, 850.0, 310.0, 1500.0]
})

# --- LIVE PRICE FETCHING ENGINE ---


# --- LIVE PRICE FETCHING ENGINE ---
@st.cache_data(ttl=60)  # Caches the data for 60 seconds so you don't hit API rate limits
def get_live_prices():
    # Fetching live USD prices from CoinGecko's public endpoint
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,stellar,osmosis,litentry,asrr&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        # Map API response names back to your asset symbols
        return {
            'BTC': response.get('bitcoin', {}).get('usd', 65000.0),
            'ETH': response.get('ethereum', {}).get('usd', 3300.0),
            'XLM': response.get('stellar', {}).get('usd', 0.12),
            'OSMO': response.get('osmosis', {}).get('usd', 0.85),
            'LIT': response.get('litentry', {}).get('usd', 0.75),
            'ASRR': response.get('asrr', {}).get('usd', 0.05)  # Fallback estimates if offline
        }
    except:
        # Emergency fallbacks if the API fails or rate-limits
        return {'BTC': 65000.0, 'ETH': 3300.0, 'XLM': 0.12, 'OSMO': 0.85, 'LIT': 0.75, 'ASRR': 0.05}

prices = get_live_prices()

# Calculate dynamic values
df['Live Price (USD)'] = df['Asset'].map(prices)
df['Total Value (USD)'] = df['Balance'] * df['Live Price (USD)']

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎯 Dashboard Filters")
selected_exchange = st.sidebar.multiselect(
    "Filter by Exchange Location:",
    options=df['Exchange'].unique(),
    default=df['Exchange'].unique()
)

# Apply filter
filtered_df = df[df['Exchange'].isin(selected_exchange)]

# --- MAIN METRIC CARDS ---
total_portfolio_value = filtered_df['Total Value (USD)'].sum()
kraken_share = filtered_df[filtered_df['Exchange'] == 'Kraken']['Total Value (USD)'].sum()
cdc_share = filtered_df[filtered_df['Exchange'] == 'Crypto.com']['Total Value (USD)'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💰 Total Portfolio Value", value=f"${total_portfolio_value:,.2f}")
with col2:
    st.metric(label="🐙 Kraken Balance", value=f"${kraken_share:,.2f}")
with col3:
    st.metric(label="🦁 Crypto.com Balance", value=f"${cdc_share:,.2f}")

st.markdown("---")

# --- CHARTS & LAYOUT VIEWS ---
left_chart_col, right_table_col = st.columns([1, 1])

with left_chart_col:
    st.subheader("📊 Asset Allocation Structure")
    if not filtered_df.empty:
        fig = px.pie(
            filtered_df, 
            values='Total Value (USD)', 
            names='Asset', 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Plotly3
        )
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select an exchange in the sidebar to populate the chart view.")

with right_table_col:
    st.subheader("📋 Active Asset Breakdown")
    # Clean up formatting for display
    display_df = filtered_df.copy()
    display_df['Balance'] = display_df['Balance'].map('{:,.2f}'.format)
    display_df['Live Price (USD)'] = display_df['Live Price (USD)'].map('${:,.2f}'.format)
    display_df['Total Value (USD)'] = display_df['Total Value (USD)'].map('${:,.2f}'.format)
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# Small status alert at footer
st.caption("🔄 Prices auto-refresh from CoinGecko API on manual page interactions.")
