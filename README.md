# Finviz API

A Python API for extracting and analyzing financial data from Finviz using web scraping.

---

## Overview

The Finviz API project enables users to extract stock tickers and fundamental financial indicators directly from Finviz.com. The API facilitates seamless integration into your financial analysis workflows, providing tools to automate and extend stock analysis tasks.

---

## Features

- **Stock Screener:** Extract stock tickers based on predefined or custom filters from Finviz.
- **Fundamental Data Extraction:** Retrieve detailed financial indicators for specific tickers.
- **Pagination Handling:** Automatically manages multi-page screener results.
- **Error Handling and Retry Logic:** Robust management of HTTP errors, including rate limiting (HTTP 429).
- **Data Export:** Easily export data into CSV format for further analysis.

---

## Installation

Clone this repository and set up the environment using [uv](https://github.com/astral-sh/uv):

```bash
git clone https://github.com/yourusername/finviz-api.git
cd finviz-api
uv venv
uv pip install requests beautifulsoup4 pandas
```

Activate your virtual environment:

```bash
source .venv/bin/activate
```

---

## Usage

### Extracting Tickers from Finviz Screener

Use the screener to obtain tickers based on predefined filters:

```python
from screener import get_total_tickers, get_finviz_stocks, BASE_URL

# Step 1: Get total tickers
total_tickers = get_total_tickers(BASE_URL)

# Step 2: Retrieve stock information
df_tickers = get_finviz_stocks(BASE_URL, total_tickers)
print(df_tickers.head())
```

### Extracting Fundamental Data

Obtain detailed fundamental indicators for tickers:

```python
from fundamentals import get_fundamentals_for_tickers

# List of tickers (example)
tickers = ['AAPL', 'TSLA', 'MSFT']

# Get fundamentals
df_fundamentals = get_fundamentals_for_tickers(tickers)
print(df_fundamentals.head())
```

---

## Output Data

- **Ticker Data**: Saved to `finviz_tickers.csv`.
- **Fundamental Data**: Saved to `finviz_fundamentals.csv`.

---

## Project Structure

```
finviz-api/
├── fundamentals.py         # Fundamental indicators extraction logic
├── screener.py             # Stock tickers scraping from Finviz screener
├── main.py                 # Entry point demonstrating API usage
└── README.md               # Project documentation
```

---

## Dependencies

Managed by **uv**:

- requests
- beautifulsoup4
- pandas

Install dependencies using:

```bash
uv pip install requests beautifulsoup4 pandas
```

---

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for improvements or bug reports.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This API performs web scraping on Finviz.com. Ensure compliance with the website’s terms of service and usage policies.

