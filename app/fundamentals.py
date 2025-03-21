import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://finviz.com/",
}

def get_fundamentals(ticker: str, max_retries=3, wait_seconds=60) -> dict:
    """
    Extrae los indicadores fundamentales manejando errores HTTP 429.

    :param ticker: Nombre del ticker (ej. 'AAPL', 'TSLA').
    :param max_retries: Máximo número de reintentos.
    :param wait_seconds: Tiempo a esperar en segundos tras error 429.
    :return: Diccionario con indicadores fundamentales.
    """
    url = f"https://finviz.com/quote.ashx?t={ticker}"

    retries = 0
    retries_attempted = 1
    while retries <= max_retries:
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 429:
            retries_left = max_retries - retries_attempted
            print(f"⚠️ HTTP 429 para {ticker}. Reintentando en {wait_seconds} segundos... (Intentos restantes: {retries_left})")
            time.sleep(wait_seconds)
            retries_attempted += 1
            continue

        if response.status_code != 200:
            print(f"⚠️ Error {response.status_code} para {ticker}. Saltando ticker.")
            return {}

        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find_all("tr", class_=["table-dark-row", "table-light-row"])

        data = {}
        for row in rows:
            columns = row.find_all("td")
            for i in range(0, len(columns), 2):
                key = columns[i].text.strip()
                value_cell = columns[i+1]

                # Si "Trades" tiene candado, se deja vacío
                if key == "Trades" and value_cell.find("svg"):
                    value = ""
                else:
                    value = value_cell.text.strip()

                data[key] = value

        return data

        retries_attempted += 1

    print(f"❌ Fallo al extraer datos de {ticker} después de {max_retries} intentos.")
    return {}



def get_fundamentals_for_tickers(tickers: list) -> pd.DataFrame:
    """
    Extrae los indicadores fundamentales para una lista de tickers usando BeautifulSoup.
    
    :param tickers: Lista de tickers a analizar.
    :return: DataFrame con los datos fundamentales.
    """
    all_data = []

    for ticker in tickers:
        print(f"🔍 Extrayendo datos de {ticker}...")
        fundamentals = get_fundamentals(ticker)

        if fundamentals:
            fundamentals["Ticker"] = ticker
            all_data.append(fundamentals)

    return pd.DataFrame(all_data)
