import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# 1. Hisse ve Döviz Havuzunun Tanımlanması (Rapor )
TICKER_LIST = {
    "GARAN.IS": "Garanti Bankasi",
    "KCHOL.IS": "Koc Holding",
    "TUPRS.IS": "Tupras",
    "EREGL.IS": "Eregli Demir Celik",
    "THYAO.IS": "Turk Hava Yollari",
    "USDTRY=X": "US Dollar / Turkish Lira",
    "EURTRY=X": "Euro / Turkish Lira"
}

# 2. Tarih Ayarları (Rapor [cite: 32])
START_DATE = "2015-01-01"  # Daha sağlıklı eğitim verisi için 2015 baz alındı
END_DATE = datetime.now().strftime('%Y-%m-%d')

def fetch_and_save_data():
    """
    Rapor [cite: 40-41] uyarınca gerçek zamanlı piyasa verilerini çeker ve saklar.
    """
    if not os.path.exists("Data_source"):
        os.makedirs("Data_source")
        print("Data_source klasörü oluşturuldu.")

    for ticker, name in TICKER_LIST.items():
        print(f"\n--- {name} ({ticker}) Verileri Çekiliyor ---")
        
        try:
            # yfinance üzerinden güncel veri indirme
            data = yf.download(ticker, start=START_DATE, end=END_DATE)
            
            if data.empty:
                print(f"HATA: {ticker} için veri seti boş döndü.")
                continue

            # CSV Kayıt İşlemi (Teknik İş Akışı )
            file_name = f"{ticker.replace('.', '_').replace('=', '_')}_data.csv"
            file_path = os.path.join("Data_source", file_name)
            data.to_csv(file_path)
            
            print(f"BAŞARILI: {len(data)} satır kaydedildi: {file_path}")

        except Exception as e:
            print(f"KRİTİK HATA [{ticker}]: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
    print("\n[BULLS] Tüm veriler güncellendi. Modelleme aşamasına hazırsınız.")