BSE Stock Candlestick Chart

A Python command-line project that fetches historical BSE stock prices from the Alpha Vantage API and displays them as OHLC candlestick charts.

Features

- Daily, weekly, and monthly historical stock data
- User-selected BSE stock symbol
- User-selected historical date range in years
- Open, high, low, and close (OHLC) candlesticks
- Chronological date sorting and numeric price conversion
- Basic handling of HTTP errors, invalid symbols, and API rate limits
- API key loaded from an environment variable or local credentials file

«The chart currently displays OHLC prices only. It does not plot trading volume or provide investment advice. Availability of a particular BSE symbol depends on Alpha Vantage's symbol coverage and API plan.»

Requirements

- Python 3.9 or later
- An Alpha Vantage API key
- Packages listed in "requirements.txt"

Setup

1. Clone or download this repository.

2. Create a virtual environment (recommended):
   
   python -m venv .venv
   
   Activate it:
   
   Windows
   
   .venv\Scripts\activate
   
   macOS/Linux
   
   source .venv/bin/activate

3. Install dependencies:
   
   python -m pip install -r requirements.txt

4. Get an API key from "Alpha Vantage" (https://www.alphavantage.co/support/#api-key).

Configure your API key

Choose one of these methods.

Option A — Environment variable

macOS/Linux:

export ALPHAVANTAGE_API_KEY="your_actual_api_key"

Windows PowerShell:

$env:ALPHAVANTAGE_API_KEY="your_actual_api_key"

Option B — Local credentials file

Copy "creds.example.json" to "creds.json", then replace the placeholder:

{
    "api_key": "your_actual_api_key"
}

The real "creds.json" file is excluded by ".gitignore". Never commit your actual API key.

Run the project

From the repository directory:

python Stocks_candle_stics.py

Enter:

- Interval: "daily", "weekly", or "monthly"
- Stock symbol: for example, "RELIANCE"
- Number of years of historical data

The script appends ".BSE" to the symbol automatically if it is not already present.

Run tests

The unit tests check interval mapping and OHLC data preparation without making live API requests:

python -m unittest discover -s tests -v

Project structure

Stocks-Candle-Stik/
│
├── Stocks_candle_stics.py
├── requirements.txt
├── README.md
├── creds.example.json
├── .gitignore
│
└── tests/
    └── test_stock_data.py

Data source

Historical stock data is retrieved from the "Alpha Vantage API" (https://www.alphavantage.co/).
