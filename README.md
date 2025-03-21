# Finviz API

A Python API built with FastAPI for extracting and analyzing financial data from Finviz using web scraping.

---

## Overview

The Finviz API project enables users to extract stock tickers and fundamental financial indicators directly from Finviz.com. It leverages FastAPI to create a robust and scalable REST API, facilitating seamless integration into your financial analysis workflows, and automating stock analysis tasks.

---

## Features

- **REST API with FastAPI:** Serve data through a simple and efficient API endpoint.
- **Stock Screener:** Extract stock tickers based on predefined or custom filters from Finviz.
- **Fundamental Data Extraction:** Retrieve detailed financial indicators for specific tickers.
- **Pagination Handling:** Automatically manages multi-page screener results.
- **Error Handling and Retry Logic:** Robust management of HTTP errors, including rate limiting (HTTP 429).
- **Data Export:** Easily export data into CSV format for further analysis.

---

## Installation

Clone this repository and install dependencies using `uv`:

```bash
git clone https://github.com/yourusername/finviz-api.git
cd finviz-api
uv venv
uv pip install .
```

Dependencies are managed in the `pyproject.toml` file.

---

## Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Visit the API documentation at:

```
http://localhost:8000/docs
```

---

## API Usage Examples

### Extracting Tickers from Finviz Screener

```bash
GET /tickers
```

### Extracting Fundamental Data

```bash
GET /fundamentals?ticker=AAPL
```

---

## Project Structure

```
finviz-api/
├── app/
│   ├── fundamentals.py        # Fundamental indicators extraction logic
│   ├── screener.py            # Stock tickers scraping from Finviz screener
│   └── schemas.py             # Pydantic schemas for data validation
├── main.py                    # FastAPI entry point
├── pyproject.toml             # Project dependencies and configuration
└── README.md                  # Project documentation
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

