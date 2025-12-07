# Data_source/fx_data_fetch.py

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

dolar_euro_tickers = ['USDTRY=X', 'EURTRY=X']
START_DATE = "2010-01-01"
END_DATE = datetime.now().strftime('%Y-%m-%d')

def fetch_fx_data():
    print("Dolar ve Euro verileri çekiliyor...")
    try:
        doviz_data = yf.download(dolar_euro_tickers, start=START_DATE, end=END_DATE)['Close']
        doviz_data.columns = ['EUR_TL', 'USD_TL'] 
        doviz_data.fillna(method='ffill', inplace=True)
        csv_yolu = os.path.join(os.path.dirname(__file__), 'dolar_euro_kurlari.csv')
        doviz_data.to_csv(csv_yolu)
        print(f"✅ Döviz kurları başarıyla '{os.path.basename(csv_yolu)}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    fetch_fx_data()