# Data_Source/data_fetch.py

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def fetch_and_save_bist_data(ticker="XU100.IS", start_date="2010-01-01", end_date=datetime.now().strftime('%Y-%m-%d')):
    """
    Belirtilen Borsa İstanbul (BIST) koduna ait tarihi verileri çeker ve kaydeder.
    """
    print(f"BIST Kodu {ticker} verileri {start_date} tarihinden itibaren çekiliyor...")
    
    try:
        # Veri çekme işlemi
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            print(f"HATA: {ticker} için veri çekilemedi veya veri seti boş.")
            return None

        # Veriyi bir CSV dosyasına kaydetme
        file_name = f"{ticker.replace('.', '_')}_data.csv"
        # Not: Kayıt yolunu ana dizinin (TRADEFIN) altına atıyoruz
        file_path = os.path.join("Data_source", file_name)
        data.to_csv(file_path)
        
        print(f"Veri çekme başarılı. Toplam {len(data)} satır veri çekildi.")
        print(f"Veri başarıyla {file_path} konumuna kaydedildi.")
        
        return data

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

# Ana işlev: BIST 100 verisini çekip kaydedelim
if __name__ == "__main__":
    bist_100_df = fetch_and_save_bist_data(ticker="XU100.IS", start_date="2010-01-01")

    if bist_100_df is not None:
        print("\nÇekilen Verinin İlk 5 Satırı:")
        print(bist_100_df.head())
        print("\nÇekilen Verinin Son 5 Satırı:")
        print(bist_100_df.tail())