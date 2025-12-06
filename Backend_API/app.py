# Backend_API/app.py

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# --- Model ve Harita Yollarını Tanımlama ---
# BASE_DIR'ı, Windows'un anladığı şekilde tanımlıyoruz (Projenizin ana dizini)
# Bu, Frontend kodunuzdaki BASE_DIR ile aynıdır:
BASE_DIR = "C:\\Users\\Berkay\\TRADEFIN" 

MODEL_PATH = os.path.join(BASE_DIR, "ML_Model", "random_forest_model.joblib")
TICKER_MAP_PATH = os.path.join(BASE_DIR, "ML_Model", "ticker_mapping.joblib")

# --- Model Yükleme ---
try:
    model = joblib.load(MODEL_PATH)
    ticker_mapping = joblib.load(TICKER_MAP_PATH)
    print("API: Model ve Ticker Haritası başarıyla yüklendi.")
except Exception as e:
    print(f"API HATA: Model yüklenemedi. {e}")
    model = None
    ticker_mapping = {}

# --- API Uç Noktası ---
@app.route('/predict', methods=['POST'])
def predict_stock_price():
    if model is None:
        return jsonify({"error": "Makine Öğrenimi Modeli Yüklenemedi."}), 500

    # 1. Kullanıcıdan Girdi Alma (Mobil uygulamadan gelecek)
    data = request.get_json()
    
    # Gerekli girdiler: Ticker (Hisse kodu) ve son günün işlem verileri
    # NOT: Mobil uygulama, modelin beklediği bu 7 feature'ı (özelliği) göndermelidir!
    required_features = ['Close', 'Open', 'High', 'Low', 'Volume', 'MA_10', 'RSI']
    
    # Temel hata kontrolü
    if 'Ticker' not in data or not all(f in data for f in required_features):
        return jsonify({"error": "Eksik parametreler. Ticker ve tüm teknik göstergeler gereklidir."}), 400

    ticker = data['Ticker']

    # 2. Girdiyi Modela Uygun Hale Getirme
    if ticker not in ticker_mapping:
        return jsonify({"error": f"Bilinmeyen hisse kodu: {ticker}"}), 400
        
    ticker_encoded = ticker_mapping[ticker]
    
    # Modelin beklediği tek satırlık DataFrame'i oluşturma
    input_data = {f: [data[f]] for f in required_features}
    input_data['Ticker_Encoded'] = [ticker_encoded]
    
    input_df = pd.DataFrame(input_data)
    
    # 3. Tahmin Yapma
    prediction = model.predict(input_df)
    
    # 4. Sonucu Döndürme
    return jsonify({
        "ticker": ticker,
        "predicted_close": round(prediction[0], 2),
        "prediction_date": (datetime.now() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    })

# --- Uygulamayı Çalıştırma ---
if __name__ == '__main__':
    # Flask'ı debug modunda çalıştırıyoruz
    app.run(debug=True, host='0.0.0.0', port=5000)