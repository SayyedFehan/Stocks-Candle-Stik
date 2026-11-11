"""Fetch BSE stock price history from Alpha Vantage and plot OHLC candles."""

import json
import os
from pathlib import Path

import matplotlib.dates as mpdates
import matplotlib.pyplot as plt
import pandas as pd
import requests
from mplfinance.original_flavor import candlestick_ohlc


API_URL = "https://www.alphavantage.co/query"

INTERVALS = {
    "DAILY": ("TIME_SERIES_DAILY", "Time Series (Daily)"),
    "WEEKLY": ("TIME_SERIES_WEEKLY", "Weekly Time Series"),
    "MONTHLY": ("TIME_SERIES_MONTHLY", "Monthly Time Series"),
}

OHLC_COLUMNS = {
    "1. open": "Open",
    "2. high": "High",
    "3. low": "Low",
    "4. close": "Close",
}


def load_api_key():
    """Read the API key from an environment variable or local creds.json."""

    api_key = os.getenv("ALPHAVANTAGE_API_KEY")

    if api_key:
        return api_key.strip()

    credentials_path = Path("creds.json")

    if not credentials_path.is_file():
        raise FileNotFoundError(
            "API key not found. Set ALPHAVANTAGE_API_KEY "
            "or create creds.json using creds.example.json."
        )

    with credentials_path.open(encoding="utf-8") as file:
        credentials = json.load(file)

    api_key = credentials.get("api_key", "").strip()

    if not api_key or api_key == "your_api_key":
        raise ValueError("Add a valid Alpha Vantage API key to creds.json.")

    return api_key


def stock_info(interval, symbol, api_key):
    """Fetch the requested BSE time series from Alpha Vantage."""

    interval = interval.upper()

    if interval not in INTERVALS:
        raise ValueError("Interval must be daily, weekly, or monthly.")

    function_name, _ = INTERVALS[interval]

    symbol = symbol.strip().upper()

    if not symbol:
        raise ValueError("Stock symbol cannot be empty.")

    if not symbol.endswith(".BSE"):
        symbol += ".BSE"

    response = requests.get(
        API_URL,
        params={
            "function": function_name,
            "symbol": symbol,
            "outputsize": "full",
            "apikey": api_key,
        },
        timeout=20,
    )

    response.raise_for_status()
    payload = response.json()

    for error_key in ("Error Message", "Note", "Information"):
        if error_key in payload:
            raise RuntimeError(
                f"Alpha Vantage: {payload[error_key]}"
            )

    series_key = INTERVALS[interval][1]

    if series_key not in payload:
        raise RuntimeError(
            f"Expected '{series_key}' in API response. "
            f"Available fields: {', '.join(payload.keys()) or 'none'}"
        )

    return payload[series_key]


def prepare_stock_dataframe(time_series, years):
    """Convert API data into chronological OHLC data."""

    if years <= 0:
        raise ValueError("Number of years must be greater than zero.")

    if not time_series:
        raise ValueError("No stock data was returned.")

    df = pd.DataFrame.from_dict(time_series, orient="index")

    missing_columns = set(OHLC_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            "Stock data is missing required fields: "
            + ", ".join(sorted(missing_columns))
        )

    df = df.rename(columns=OHLC_COLUMNS)

    df.index = pd.to_datetime(df.index, errors="coerce")

    df = df.loc[
        ~df.index.isna(),
        ["Open", "High", "Low", "Close"]
    ]

    df = df.apply(pd.to_numeric, errors="coerce").dropna()

    df = df.sort_index()

    cutoff_date = (
        pd.Timestamp.today().normalize()
        - pd.DateOffset(years=years)
    )

    df = df.loc[df.index >= cutoff_date]

    if df.empty:
        raise ValueError(
            "No stock data is available for the selected date range."
        )

    df.index.name = "Date"

    return df.reset_index()


def plot_candlestick(df, symbol, interval, years):
    """Display an OHLC candlestick chart."""

    chart_data = df.copy()

    chart_data["Date"] = chart_data["Date"].map(
        mpdates.date2num
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    candlestick_ohlc(
        ax,
        chart_data[
            ["Date", "Open", "High", "Low", "Close"]
        ].values,
        width=0.6,
        colorup="green",
        colordown="red",
        alpha=0.8,
    )

    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    ax.set_title(
        f"{symbol} - {interval.title()} OHLC ({years} year(s))"
    )

    ax.xaxis.set_major_formatter(
        mpdates.DateFormatter("%d-%m-%Y")
    )

    fig.autofmt_xdate()
    fig.tight_layout()

    plt.show()


def main():
    try:
        api_key = load_api_key()

        interval = input(
            "Data interval (daily, weekly, or monthly): "
        ).strip().upper()

        symbol = input(
            "BSE stock symbol (for example, RELIANCE): "
        ).strip().upper()

        years = int(
            input("Number of years of data: ").strip()
        )

        if years <= 0:
            raise ValueError(
                "Number of years must be greater than zero."
            )

        time_series = stock_info(interval, symbol, api_key)

        df = prepare_stock_dataframe(time_series, years)

        plot_candlestick(df, symbol, interval, years)

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
        requests.RequestException,
    ) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
