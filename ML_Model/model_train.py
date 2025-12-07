# ML_Model/model_train.py (GÜNCEL VERSİYON)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import os
import glob
import joblib 

# --- PATH VE DOSYA AYARLARI ---
# Betiğin bulunduğu yerden Data_source/Processed_Data klasörüne giden mutlak yol
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'Data_source', 'Processed_Data')

# Model ve Ticker eşleme dosyalarının kayıt yolu (ML_Model klasörünün içine kaydeder)
MODEL_PATH = os.path.join(CURRENT_DIR, "random_forest_model.joblib")
MAPPER_PATH = os.path.join(CURRENT_DIR, "ticker_mapping.joblib")

# Modelleri kaydetmek için klasörü oluştur
if not os.path.exists(CURRENT_DIR):
    os.makedirs(CURRENT_DIR)

# --- VERİ YÜKLEME ---

def load_and_combine_data():
    """Döviz kurlarıyla birleştirilmiş veri setlerini okur ve tek bir DataFrame'de birleştirir."""
    
    # Yeni oluşturulan *_final_processed.csv dosyalarını bulur
    # BURADA GÜNCEL DOSYA ADI KULLANILIYOR: *_final_processed.csv
    all_files = glob.glob(os.path.join(PROCESSED_DATA_DIR, "*_final_processed.csv"))
    
    if not all_files:
        print(f"HATA: Processed_Data klasöründe hiç *_final_processed.csv verisi bulunamadı! Lütfen data_merger_fx.py'yi çalıştırın.")
        return None
        
    all_data = []
    
    for file_path in all_files:
        df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
        df['Ticker'] = os.path.basename(file_path).split('_')[0]
        all_data.append(df)
        
    combined_df = pd.concat(all_data)
    combined_df.dropna(inplace=True)
    
    print(f"Tüm veriler birleştirildi. Toplam satır: {len(combined_df)}")
    return combined_df

# --- MODEL EĞİTİMİ ---

def train_and_save_model(data_df):
    """Random Forest modelini yeni özelliklerle eğitir ve kaydeder."""

    # Ticker sütununu sayısal kategoriye dönüştür
    data_df['Ticker_Encoded'] = data_df['Ticker'].astype('category').cat.codes

    # 1. Özellikleri (X) ve Hedefi (Y) Belirleme
    features = [
        'Close', 'Open', 'High', 'Low', 'Volume', 
        'MA_10', 'RSI', 'Ticker_Encoded',
        
        # 👇 YENİ EKLEDİKLERİMİZ
        'USD_TL',  # Dolar/TL kuru
        'EUR_TL'   # Euro/TL kuru
    ]
    target = 'Target_Close'
    
    X = data_df[features]
    Y = data_df[target]

    # 2. Eğitim ve Test Kümelerine Ayırma (Zamana bağlı ayırma)
    split_point = int(len(X) * 0.80)
    X_train, X_test = X[:split_point], X[split_point:]
    Y_train, Y_test = Y[:split_point], Y[split_point:]
    
    print(f"Eğitim seti boyutu: {len(X_train)}, Test seti boyutu: {len(X_test)}")

    # 3. Random Forest Modelini Eğitme
    print("Model eğitimi başlıyor (Dolar/Euro dahil)...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, Y_train)
    print("Model eğitimi tamamlandı.")

    # 4. Performansı Değerlendirme
    predictions = model.predict(X_test)
    mse = mean_squared_error(Y_test, predictions)
    r2 = r2_score(Y_test, predictions)

    print(f"\n--- Model Performansı ---")
    print(f"Hata Kare Ortalaması (MSE): {mse:.2f}")
    print(f"R-Kare Skoru (R2): {r2:.2f}")

    # 5. Modeli Kaydetme
    joblib.dump(model, MODEL_PATH)
    
    # Modelin kullandığı Ticker kodlamasını da kaydetme (Backend API için kritik)
    ticker_mapping = data_df[['Ticker', 'Ticker_Encoded']].drop_duplicates().set_index('Ticker').to_dict()['Ticker_Encoded']
    joblib.dump(ticker_mapping, MAPPER_PATH)
    
    print(f"\nModel ve Eşleyici başarıyla kaydedildi: {os.path.basename(MODEL_PATH)} ve {os.path.basename(MAPPER_PATH)}")

# --- ANA ÇALIŞTIRMA ---
if __name__ == "__main__":
    combined_data = load_and_combine_data()
    if combined_data is not None:
        train_and_save_model(combined_data)