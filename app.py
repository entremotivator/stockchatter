import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Search App", layout="wide")
st.title("📈 Stock Search & Info with yFinance")

# Sidebar for ticker input
ticker = st.sidebar.text_input("Enter Stock Ticker Symbol", value="AAPL", max_chars=10)

# Date selection
end_date = datetime.today()
start_date = end_date - timedelta(days=180)

# Fetch stock data
def fetch_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        info = stock.info
        return stock, hist, info
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None, None

if ticker:
    stock, hist, info = fetch_stock(ticker)

    if hist is not None and not hist.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"{info.get('longName', 'Unknown Company')} ({ticker.upper()})")
            st.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
            st.line_chart(hist['Close'], use_container_width=True)

        with col2:
            st.subheader("📋 Company Info")
            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
            st.write(f"**Market Cap:** {info.get('marketCap', 'N/A'):,}")
            st.write(f"**Website:** [{info.get('website', '')}]({info.get('website', '')})")

            st.markdown("**📄 Description:**")
            st.write(info.get('longBusinessSummary', 'N/A'))

    else:
        st.warning("No historical data found for this ticker.")
else:
    st.info("Please enter a stock ticker symbol in the sidebar.")

