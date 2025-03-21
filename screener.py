import math
import re
from typing import List
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base de Finviz con filtros aplicados
BASE_URL = "https://finviz.com/screener.ashx?v=111&f=fa_fpe_low,fa_pe_low,fa_ps_u2"
# https://finviz.com/screener.ashx?v=111&f=fa_fpe_low,fa_pe_low,fa_ps_u2&ft=2

# Headers para evitar bloqueos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://finviz.com/",
    "DNT": "1",
    "Connection": "keep-alive",
}

def get_total_tickers(url: str):
    """Obtiene el número total de tickers listados en Finviz."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: Código de estado {response.status_code}")
        return 0

    soup = BeautifulSoup(response.text, "html.parser")
    total_tickers_element = soup.find("div", id="screener-total")

    if total_tickers_element:
        text = total_tickers_element.text.strip()
        total = int(text.split("/")[1].split()[0])  # Extrae el número total
        return total
    else:
        print("No se encontró el total de tickers en la página.")
        return 0

def is_valid_ticker(ticker: str) -> bool:
    """Verifica si el ticker es válido (permite letras, números y guiones)."""
    return bool(re.match(r"^[A-Za-z0-9\-]+$", ticker))

def clean_ticker(raw_ticker: str) -> str:
    """Elimina el número de índice antes del ticker en cada página."""
    parts = raw_ticker.split()  
    return parts[-1] if len(parts) > 1 else raw_ticker  

def get_ticker_list(df: pd.DataFrame) -> List[str]:
    """
    Extrae la lista de tickers desde un DataFrame.
    
    :param df: DataFrame con los datos de Finviz.
    :return: Lista de tickers en formato de cadena.
    """
    if "Ticker" in df.columns:
        return df["Ticker"].tolist()  # Devuelve solo los tickers como lista
    
    print("Error: La columna 'Ticker' no existe en el DataFrame.")
    return []

def get_finviz_stocks(url: str, total_tickers: int):
    """Extrae todas las empresas en varias páginas de Finviz, evitando encabezados repetidos."""
    stocks = []
    per_page = 20  
    total_pages = math.ceil(total_tickers / per_page)  

    for page in range(total_pages):
        start_row = page * per_page + 1  
        paginated_url = f"{url}&r={start_row}"  

        print(f"Scraping página {page + 1}/{total_pages} - URL: {paginated_url}")

        response = requests.get(paginated_url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error en la página {page + 1}: Código {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("tr", id="screener-table")  # ✅ Usamos el ID correcto
        
        if not table:
            print(f"No se encontró la tabla en la página {page + 1}.")
            continue

        rows = table.find_all("tr")

        if not rows or len(rows) < 2:
            print(f"La tabla en la página {page + 1} está vacía.")
            continue

        for i, row in enumerate(rows[1:]):  # ✅ Saltamos la primera fila de cada página
            columns = row.find_all("td")
            if len(columns) < 10:
                continue

            raw_ticker = columns[1].text.strip()  
            clean_ticker_value = clean_ticker(raw_ticker)  

            # ✅ Filtramos filas no válidas
            if not is_valid_ticker(clean_ticker_value) or clean_ticker_value == "Ticker":
                continue

            stock_data = {
                "Ticker": clean_ticker_value,
                "Company": columns[2].text.strip(),
                "Sector": columns[3].text.strip(),
                "Industry": columns[4].text.strip(),
                "Country": columns[5].text.strip(),
                "Market Cap": columns[6].text.strip(),
                "P/E": columns[7].text.strip(),
                "Price": columns[8].text.strip(),
                "Change": columns[9].text.strip(),
                "Volume": columns[10].text.strip(),
            }

            stocks.append(stock_data)

    return pd.DataFrame(stocks)
