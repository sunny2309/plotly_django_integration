from django.shortcuts import render, redirect
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.io import to_html

tickers = ["AAPL", "NVDA", "GOOGL", "MSFT", "BAC", "META", "AMZN",
            "NFLX", "ADBE", "TSLA", "JPM", "CRM", "CSCO", "NKE", "QCOM"]
names = ['Apple Inc.', 'NVIDIA Corporation', 'Alphabet Inc.', 'Microsoft Corporation',
 'Bank of America Corporation', 'Meta Platforms, Inc.', 'Amazon.com, Inc.',
 'Netflix, Inc.', 'Adobe Inc.', 'Tesla, Inc.', 'JPMorgan Chase & Co.',
 'Salesforce, Inc.', 'Cisco Systems, Inc.', 'NIKE, Inc.', 'QUALCOMM Incorporated']

def index(request):
    return redirect("stock_dashboard:display_ticker", "AAPL")

def retrieve_stock_data(ticker:str):
    ticker_obj = yf.Ticker(ticker)    
    ticker_info =ticker_obj.info
    ## Historical Data
    hist_df = ticker_obj.history(period="3mo")
    hist_df = hist_df.reset_index()

    return hist_df, ticker_info

def create_candlestick_chart(hist_df: pd.DataFrame):
    fig = go.Figure(data=[
                        go.Candlestick(
                            x=hist_df['Date'],
                            open=hist_df['Open'],
                            high=hist_df['High'],
                            low=hist_df['Low'],
                            close=hist_df['Close'])
                ])
    fig.update_layout(margin={"t":0, "l":0, "r":0, "b":0})

    return fig

def display_ticker(request, ticker: str):
    hist_df, info = retrieve_stock_data(ticker)
    candlestick_fig = create_candlestick_chart(hist_df)
    chart_div = to_html(candlestick_fig, full_html=False, 
                        include_plotlyjs="cdn", div_id="ohlc")

    p1, p2 = hist_df["Close"].values[-1], hist_df["Close"].values[-2]
    change, prcnt_change = (p2-p1), (p2-p1) / p1

    context = {
                "tickers": zip(tickers, names),
                "ticker": ticker,
                "chart_div": chart_div,
                "name": info["longName"],
                "industry": info["industry"],
                "sector": info["sector"],
                "summary": info["longBusinessSummary"],
                "close": f"{p1: .2f} USD",
                "change": f"{change:.2f}",
                "pct_change": f"{prcnt_change*100:.2f}%"
                }
    return render(request, "stock_dashboard/ticker_analysis.html", context)