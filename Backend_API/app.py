# Backend_API/app.py - NİHAİ VERSİYON (Tüm İsteKleri İçerir)

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
import numpy as np # CAGR hesaplaması için gerekli

app = Flask(__name__)

# --- Model ve Harita Yollarını Tanımlama ---
# Projenizin ana dizinini Windows'a uygun şekilde tanımlama
BASE_DIR = "C:\\Users\\Berkay\\TRADEFIN" 

MODEL_DIR = os.path.join(BASE_DIR, "ML_Model")
MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_model.joblib")
TICKER_MAP_PATH = os.path.join(MODEL_DIR, "ticker_mapping.joblib")
LONG_FX_MODEL_PATH = os.path.join(MODEL_DIR, "long_term_fx_model.joblib") 

# --- Model Yükleme ---
try:
    # Random Forest Modelini yükle
    stock_predictor = joblib.load(MODEL_PATH)
    ticker_mapping = joblib.load(TICKER_MAP_PATH)
    print("API: Random Forest Model ve Ticker Haritası başarıyla yüklendi.")
except Exception as e:
    print(f"API HATA: Random Forest Model yüklenemedi. {e}")
    stock_predictor = None
    ticker_mapping = {}

# NOT: long_fx_predictor artık global olarak yüklenmiyor, çağrıldığında yükleniyor (güvenlik için)

# --- YARDIMCI FONKSİYONLAR ---

def fetch_real_time_fx():
    """Anlık Dolar ve Euro kurlarını çeker."""
    fx_tickers = ['USDTRY=X', 'EURTRY=X']
    
    try:
        # yfinance ile anlık veriyi çekme
        fx_data = yf.download(fx_tickers, period="1d")['Close'].iloc[-1].to_dict()
        return {
            "USD_TL": fx_data.get('USDTRY=X'),
            "EUR_TL": fx_data.get('EURTRY=X')
        }
    except Exception:
        return {"USD_TL": None, "EUR_TL": None}

def calculate_input_features(latest_data_series, fx_rates, ticker_encoded):
    """Tahmin için modelin beklediği DataFrame'i hazırlar."""
    # Modelin beklediği tüm 10 özellik (Close'dan EUR_TL'ye kadar) buraya dahil edilmeli
    input_features = {
        'Close': [latest_data_series['Close']],
        'Open': [latest_data_series['Open']],
        'High': [latest_data_series['High']],
        'Low': [latest_data_series['Low']],
        'Volume': [latest_data_series['Volume']],
        'MA_10': [latest_data_series['MA_10']],
        'RSI': [latest_data_series['RSI']], 
        'Ticker_Encoded': [ticker_encoded],
        'USD_TL': [fx_rates['USD_TL']],
        'EUR_TL': [fx_rates['EUR_TL']]
    }
    
    return pd.DataFrame(input_features)

# --- 5. API UÇ NOKTALARI (ROUTES) ---

@app.route('/api/predict', methods=['POST'])
def predict_stock_price():
    """Hisse senedi için bir sonraki gün kapanış fiyatını tahmin eder."""
    if stock_predictor is None:
        return jsonify({"error": "Makine Öğrenimi Modeli Yüklenemedi."}), 500

    data = request.get_json()
    required_features = ['Close', 'Open', 'High', 'Low', 'Volume', 'MA_10', 'RSI'] 
    
    if 'Ticker' not in data or not all(f in data for f in required_features):
        return jsonify({"error": "Eksik parametreler. Ticker ve son günün tüm teknik göstergeleri gereklidir."}), 400

    ticker = data['Ticker']
    
    if ticker not in ticker_mapping:
        return jsonify({"error": f"Bilinmeyen hisse kodu: {ticker}"}), 400
        
    try:
        # 1. Anlık Kur Verisini Çekme
        fx_rates = fetch_real_time_fx()
        if fx_rates['USD_TL'] is None:
            return jsonify({"error": "Anlık Dolar/Euro kurları çekilemedi."}), 500
            
        # 2. Girdiyi Modela Uygun Hale Getirme
        ticker_encoded = ticker_mapping[ticker]
        latest_data_series = pd.Series(data) 
        input_df = calculate_input_features(latest_data_series, fx_rates, ticker_encoded)
        
        # 3. Tahmin Yapma
        prediction = stock_predictor.predict(input_df)
        
        # 4. Sonucu Döndürme
        return jsonify({
            "ticker": ticker,
            "predicted_close": round(prediction[0], 2),
            "prediction_date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            "kullanilan_usd_tl": round(fx_rates['USD_TL'], 2)
        })

    except Exception as e:
        print(f"Tahmin hatası: {e}")
        return jsonify({"error": f"Tahmin sırasında bilinmeyen bir hata oluştu: {str(e)}"}), 500


@app.route('/api/fx/current', methods=['GET'])
def get_current_fx():
    """Anlık Dolar ve Euro kurlarını döndürür (Web panosundaki anlık değişimler için)."""
    fx_rates = fetch_real_time_fx()
    
    if fx_rates['USD_TL'] is None:
         return jsonify({"error": "Anlık Dolar/Euro kurları çekilemedi."}), 500

    return jsonify({
        "USD_TL": round(fx_rates['USD_TL'], 2),
        "EUR_TL": round(fx_rates['EUR_TL'], 2)
    })


@app.route('/api/fx/long_term', methods=['GET'])
def get_long_term_fx():
    """
    İstenilen: Uzun vadeli kur projeksiyonu.
    Query parametresi: ?target_date=YYYY-MM-DD
    """
    # Projeksiyon verilerini yükle
    try:
        fx_projections = joblib.load(LONG_FX_MODEL_PATH)
    except Exception as e:
        print(f"Uzun vadeli FX projeksiyon verisi yüklenemedi: {e}")
        return jsonify({"error": "Uzun vadeli FX projeksiyon verisi hazır değil. long_term_fx_model.py'yi çalıştırın."}), 503

    # 2. Query Parametresini Kontrol Etme
    target_date_str = request.args.get('target_date')
    
    # 2.A: Spesifik Tarih İsteği (Örn: 2026-01-05)
    if target_date_str:
        try:
            target_date = pd.to_datetime(target_date_str)
            
            # Projeksiyon başlangıç verilerini timeline'ın ilk ve son noktasından alıyoruz
            usd_start_date = pd.to_datetime(fx_projections['PROJECTION_START'])
            
            # Kaydedilen CAGR oranları
            usd_cagr = fx_projections['USD_CAGR']
            eur_cagr = fx_projections['EUR_CAGR']

            # En son bilinen kur değeri (Timeline'ın ilk noktası, yani bugünün kuru)
            last_usd_rate = fx_projections['USD_TL_TIMELINE'][0]['Value']
            last_eur_rate = fx_projections['EUR_TL_TIMELINE'][0]['Value']
            
            # Güncel tarihten hedef tarihe kadar geçen yıl sayısı
            proj_years = (target_date - usd_start_date).days / 365.25
            
            # Geçmiş bir tarih istenirse hata ver
            if proj_years < 0:
                return jsonify({"error": "Tahmin tarihi bugünden sonra olmalıdır."}), 400
            
            # Projeksiyon hesaplama
            predicted_usd = last_usd_rate * ((1 + usd_cagr) ** proj_years)
            predicted_eur = last_eur_rate * ((1 + eur_cagr) ** proj_years)

            return jsonify({
                "tahmin_tarihi": target_date_str,
                "usd_tl_tahmini": round(predicted_usd, 2),
                "eur_tl_tahmini": round(predicted_eur, 2),
                "tip": "Spesifik Tarih Projeksiyonu"
            })
            
        except Exception as e:
            return jsonify({"error": f"Tarih formatı veya hesaplama hatası: {str(e)}"}), 400

    # 2.B: Tüm Zaman Çizelgesi İsteği (Web Grafiği için)
    else:
        return jsonify({
            "USD_TL_Timeline": fx_projections['USD_TL_TIMELINE'],
            "EUR_TL_Timeline": fx_projections['EUR_TL_TIMELINE'],
            "başlangıç_tarihi": fx_projections['PROJECTION_START'],
            "tip": "Tüm Zaman Çizelgesi"
        })


@app.route('/api/history/<ticker>', methods=['GET'])
def get_history(ticker):
    """Grafik çizimi için hissenin son 90 günlük geçmişini döndürür."""
    
    ticker_yf = f"{ticker}.IS"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90) 
    
    try:
        data = yf.download(ticker_yf, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        
        if data.empty:
            return jsonify({"error": f"Geçmiş veri çekilemedi: {ticker}"}), 404
        
        # Sadece grafik için gerekli olan verileri döndür
        history_data = data[['Close']].reset_index()
        history_data['Date'] = history_data['Date'].dt.strftime('%Y-%m-%d')
        
        return jsonify(history_data.to_dict('records'))

    except Exception:
        return jsonify({"error": "Geçmiş veri çekilirken hata oluştu."}), 500


if __name__ == '__main__':
    # Flask'ı debug modunda çalıştırıyoruz
    app.run(debug=True, host='0.0.0.0', port=5000)