from fastapi import FastAPI
from screener import (
    get_total_tickers,
    get_finviz_stocks,
    get_ticker_list,
    BASE_URL as SCREENER_URL
)
from fundamentals import get_fundamentals_for_tickers

app = FastAPI()

@app.get("/stocks")
async def get_stocks():
    total_tickers = get_total_tickers(SCREENER_URL)
    if total_tickers == 0:
        return {"message": "No se obtuvieron tickers desde el screener."}
    df_stocks = get_finviz_stocks(SCREENER_URL, total_tickers)
    return df_stocks.to_dict(orient="records")

@app.get("/fundamentals")
async def get_fundamentals():
    total_tickers = get_total_tickers(SCREENER_URL)
    df_stocks = get_finviz_stocks(SCREENER_URL, total_tickers)
    tickers = get_ticker_list(df_stocks)
    df_fundamentals = get_fundamentals_for_tickers(tickers)
    return df_fundamentals.to_dict(orient="records")

@app.get("/fundamental/{ticker}")
async def get_fundamental(ticker: str):
    df_fundamental = get_fundamentals_for_tickers([ticker])
    return df_fundamental.to_dict(orient="records")

# def main():
#     # Paso 1: Obtener tickers desde Finviz (screener.py)
#     total_tickers = get_total_tickers(SCREENER_URL)
#     if total_tickers == 0:
#         print("No se obtuvieron tickers desde el screener.")
#         return

#     print(f"✅ Total tickers obtenidos: {total_tickers}")

#     df_tickers = get_finviz_stocks(SCREENER_URL, total_tickers)
#     if df_tickers.empty:
#         print("No se obtuvieron tickers válidos.")
#         return

#     # Guardar los tickers para referencia
#     df_tickers.to_csv("finviz_tickers.csv", index=False)

#     # Extraer lista de tickers
#     tickers = get_ticker_list(df_tickers)
    
#     # # Paso 2: Construir los fundamentales para cada ticker
#     # fundamentales = []
#     # for ticker in tickers:
#     #     stock = finvizfinance(ticker)
#     #     fundamentales.append(stock.ticker_fundament())
    
#     # df_fundamentals = pd.DataFrame(fundamentales)

    

#     # Paso 2: Obtener indicadores fundamentales (fundamentals.py)
#     df_fundamentals = get_fundamentals_for_tickers(tickers)

#     if df_fundamentals.empty:
#         print("No se obtuvieron fundamentales válidos.")
#         return

#     # Guardar los fundamentales para referencia
#     df_fundamentals.to_csv("finviz_fundamentals.csv", index=False)

#     # Confirmación
#     print("✅ Proceso completado exitosamente.")
#     print(f"Total tickers extraídos: {len(tickers)}")
#     print(f"Datos fundamentales extraídos: {df_fundamentals.shape}")

# if __name__ == "__main__":
#     main()
