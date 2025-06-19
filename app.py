import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import date, timedelta

# Page settings
st.set_page_config(page_title="📊 Stock Tracker", layout="wide")
st.title("📊 Stock Tracker & Insights")

# Sidebar inputs
with st.sidebar:
    st.header("🔍 Search Stock")
    ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL)", value="AAPL", max_chars=10)
    st.write("📅 Select Date Range:")
    start_date = st.date_input("Start Date", date.today() - timedelta(days=180))
    end_date = st.date_input("End Date", date.today())

# Fetch stock data
@st.cache_data
def load_stock_data(ticker, start, end):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start, end=end)
        info = stock.info
        return stock, hist, info
    except Exception as e:
        return None, None, {}

# Load data
stock, hist, info = load_stock_data(ticker, start_date, end_date)

if stock and not hist.empty:
    col1, col2 = st.columns([2, 1])

    # Main company info
    with col1:
        st.subheader(f"{info.get('longName', ticker.upper())} ({ticker.upper()})")
        st.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
        st.plotly_chart(
            go.Figure(
                data=go.Scatter(x=hist.index, y=hist["Close"], mode='lines', name='Close'),
                layout=go.Layout(title="📈 Closing Price", xaxis_title="Date", yaxis_title="Price (USD)")
            ),
            use_container_width=True
        )

    # Financial details
    with col2:
        st.subheader("📌 Key Metrics")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Market Cap:** {info.get('marketCap', 0):,}")
        st.write(f"**Volume:** {info.get('volume', 'N/A'):,}")
        st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
        st.write(f"**52-Week Range:** {info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.write(f"**Day Range:** {info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}")
        st.write(f"**Website:** [{info.get('website', '')}]({info.get('website', '')})")

    # Business Summary
    with st.expander("📄 Company Description"):
        st.write(info.get('longBusinessSummary', 'N/A'))

else:
    st.warning("⚠️ No data found. Please check the ticker or try a different one.")


