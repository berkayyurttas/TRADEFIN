# ML_Model/long_term_fx_model.py - NİHAİ VERSİYON (ZAMAN ÇİZELGESİ)

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression 

# --- PATH AYARLARI ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_SOURCE_PATH = os.path.join(BASE_DIR, 'Data_source', 'dolar_euro_kurlari.csv')
MODEL_SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'long_term_fx_model.joblib')

# --- PROJEKSİYON FONKSİYONLARI ---

def calculate_projection_timeline(fx_data_series, target_date_str='2027-12-31', freq='Q'):
    """Verilen seriye göre CAGR hesaplar ve hedef tarihe kadar çeyreklik projeksiyon yapar."""
    
    fx_data_series = fx_data_series.dropna()
    start_value = fx_data_series.iloc[0]
    end_value = fx_data_series.iloc[-1]
    
    start_date = fx_data_series.index.min()
    end_date = fx_data_series.index.max()
    
    time_delta = (end_date - start_date).days
    num_years = time_delta / 365.25

    # Bileşik Yıllık Büyüme Oranını (CAGR) Hesaplama
    cagr_rate = ((end_value / start_value) ** (1 / num_years)) - 1
    
    # 1. Projeksiyon için Tarih Aralıklarını Belirleme
    target_date = pd.to_datetime(target_date_str)
    
    # Bugünün tarihinden hedef tarihe kadar çeyreklik aralıklar oluşturma
    # Not: Başlangıç noktası olarak son veri tarihini alıyoruz.
    future_dates = pd.date_range(start=end_date, end=target_date, freq=freq)
    
    projections = []
    
    for date in future_dates:
        # Son veri tarihinden projeksiyon tarihine kadar geçen yıl sayısı
        proj_years = (date - end_date).days / 365.25
        
        # Projeksiyon değeri
        projected_value = end_value * ((1 + cagr_rate) ** proj_years)
        
        projections.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Value': projected_value
        })
        
    return projections, cagr_rate

def train_long_term_fx_model():
    print("➡️ Uzun Vadeli FX Modeli Eğitimi Başlıyor (Zaman Çizelgesi Projeksiyonu)...")
    
    try:
        fx_data = pd.read_csv(DATA_SOURCE_PATH, index_col=0, parse_dates=True)
    except FileNotFoundError:
        print(f"HATA: FX Veri dosyası bulunamadı: {DATA_SOURCE_PATH}")
        return

    fx_data = fx_data.dropna()
    
    # Projeksiyonları hesaplama
    usd_timeline, usd_cagr = calculate_projection_timeline(fx_data['USD_TL'])
    eur_timeline, eur_cagr = calculate_projection_timeline(fx_data['EUR_TL'])

    # Sonuçları API'nin kolayca yükleyeceği bir sözlük içinde kaydetme
    result_data = {
        'USD_TL_TIMELINE': usd_timeline,
        'EUR_TL_TIMELINE': eur_timeline,
        'USD_CAGR': usd_cagr,
        'EUR_CAGR': eur_cagr,
        'PROJECTION_START': fx_data.index.max().strftime('%Y-%m-%d')
    }
    
    joblib.dump(result_data, MODEL_SAVE_PATH)
    
    print(f"✅ Uzun Vadeli FX Projeksiyonu zaman çizelgesi olarak kaydedildi.")
    print(f"   USD/TL Projeksiyon Başlangıç Değeri: {fx_data['USD_TL'].iloc[-1]:.2f} TL")
    print(f"   EUR/TL Projeksiyon Bitiş Değeri (2027 Sonu): {eur_timeline[-1]['Value']:.2f} TL")
    
if __name__ == "__main__":
    train_long_term_fx_model()