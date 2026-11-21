import streamlit as st   # add at top with other imports, the rest at the bottom

st.set_page_config(
    page_title="MarketPulse",
    page_icon="📈",
    layout="wide"
)


st.markdown("""
<style>

/* Main dashboard background */
.stApp {
    background-color: #0B1220;
    color: #F8FAFC;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #151F32;
}

/* Make sidebar text readable */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p {
    color: #F8FAFC !important;
}

/* Headings */
h1, h2, h3 {
    color: #F8FAFC;
    font-weight: 600;
}

/* Performance metric cards */
div[data-testid="stMetric"] {
    background-color: #151F32;
    border: 1px solid #263449;
    border-radius: 12px;
    padding: 20px;
}

/* Make metric numbers white */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: white !important;
}

/* Make metric labels light gray */
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] label * {
    color: #94A3B8 !important;
}

/* Download buttons */
.stDownloadButton > button {
    background-color: #14B8A6;
    color: #07111F;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 12px 24px;
}

/* Tab labels */
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 500;
}

/* Active tab */
.stTabs [aria-selected="true"] {
    color: #14B8A6;
}


/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Chart container styling */
[data-testid="stVegaLiteChart"] {
    background-color: #151F32;
    border-radius: 12px;
    padding: 12px;
}

/* Make inactive tabs readable */
.stTabs [data-baseweb="tab"] {
    color: #94A3B8 !important;
}

/* Highlight selected tab */
.stTabs [aria-selected="true"] {
    color: #14B8A6 !important;
}

</style>
""", unsafe_allow_html=True)

import yfinance as yf
import pandas as pd
import numpy as np

def fetch_data(tickers, start_date, end_date):
    data_frames = []
    for ticker in tickers:
        stock_data = yf.download(ticker, start=start_date, end=end_date)['Close']
        data_frames.append(stock_data)
    
    data = pd.concat(data_frames, axis=1, keys=tickers)
    data.columns = tickers
    return data

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    portfolio_return = returns.mean().mean()
    portfolio_volatility = returns.std().mean()
    return (portfolio_return - risk_free_rate) / portfolio_volatility

def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    portfolio_return = returns.mean().mean()
    downside_returns = returns[returns < 0]
    downside_deviation = downside_returns.std().mean()
    return (portfolio_return - risk_free_rate) / downside_deviation

def portfolio_optimization(returns):
    return np.ones(len(returns.columns)) / len(returns.columns)

st.title("📈 MarketPulse")
st.caption("Financial Markets & Portfolio Analytics")

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Portfolio Settings")

    tickers = st.text_input(
        "Enter Stock Tickers",
        "AAPL, MSFT, GOOG"
    ).split(",")

    tickers = [ticker.strip() for ticker in tickers]

    start_date = st.date_input(
        "Start Date",
        pd.to_datetime("2020-01-01")
    )

    end_date = st.date_input(
        "End Date",
        pd.to_datetime("2023-01-01")
    )

# Fetch stock data
stock_data = fetch_data(tickers, start_date, end_date)
returns_data = stock_data.pct_change().dropna()

# Visualizations
tab1, tab2 = st.tabs([
    "📈 Stock Prices",
    "📉 Daily Returns"
])

with tab1:
    st.subheader("Stock Price Performance")
    st.line_chart(
        stock_data,
        height=400,
        use_container_width=True
    )

with tab2:
    st.subheader("Daily Stock Returns")
    st.line_chart(
        returns_data,
        height=350,
        use_container_width=True
    )

sharpe_ratio = calculate_sharpe_ratio(returns_data)
sortino_ratio = calculate_sortino_ratio(returns_data)

st.subheader("📊 Performance Metrics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

with col2:
    st.metric("Sortino Ratio", f"{sortino_ratio:.2f}")

optimal_weights = portfolio_optimization(returns_data)

st.subheader("💼 Portfolio Allocation")

allocation_data = pd.DataFrame({
    "Stock": tickers,
    "Weight": optimal_weights
})

st.write("Portfolio Weight Distribution")

st.bar_chart(
    allocation_data.set_index("Stock"),
    height=300
)

st.dataframe(
    allocation_data.style.format({"Weight": "{:.2%}"}),
    hide_index=True,
    use_container_width=True
)

csv_data = stock_data.to_csv()
st.download_button("Download Stock Data CSV", csv_data, "stock_data.csv")
