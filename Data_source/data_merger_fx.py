# Data_source/data_merger_fx.py

import pandas as pd
import glob
import os

# Mevcut betik Data_source klasöründe olduğu için kök yolu burasıdır
BASE_DIR = os.path.dirname(__file__)
PROCESSED_DIR = os.path.join(BASE_DIR, 'Processed_Data')

# 1. Döviz verisini yükleme (Data_source klasöründen)
try:
    doviz_data = pd.read_csv(os.path.join(BASE_DIR, 'dolar_euro_kurlari.csv'), index_col=0)
    doviz_data.index = pd.to_datetime(doviz_data.index)
except FileNotFoundError:
    # Bu hata gelmemeli, çünkü bir önceki adımda fx_data_fetch.py çalıştı
    print("Hata: 'dolar_euro_kurlari.csv' dosyası bulunamadı. Lütfen kontrol edin.")
    exit()

doviz_kolonlari = ['USD_TL', 'EUR_TL']

# 2. Tüm işlenmiş hisse senedi dosyalarını bulma (Processed_Data alt klasöründen)
islenmis_dosyalar = glob.glob(os.path.join(PROCESSED_DIR, '*_processed.csv'))

if not islenmis_dosyalar:
    print("Hata: Processed_Data klasöründe hiç (*_processed.csv) dosyası bulunamadı. Ön işleme yaptınız mı?")
    exit()

for dosya_yolu in islenmis_dosyalar:
    
    dosya_adi = os.path.basename(dosya_yolu)
    hisse_kodu = dosya_adi.split('_')[0]
    
    print(f"➡️ {hisse_kodu} verisi döviz kurlarıyla birleştiriliyor...")
    
    hisse_data = pd.read_csv(dosya_yolu, index_col=0, parse_dates=True)

    # Veri Setlerini Birleştirme (Tarih bazında)
    birlestirilmis_data = hisse_data.merge(doviz_data[doviz_kolonlari], 
                                          left_index=True, 
                                          right_index=True, 
                                          how='left') 
    
    # Eksik Değerleri Doldurma (Önceki günün kuru ile)
    # Bu hata verdiğinde "dovest_kolonlari" yerine "doviz_kolonlari" yazmıştım, şimdi doğru.
    birlestirilmis_data[doviz_kolonlari] = birlestirilmis_data[doviz_kolonlari].fillna(method='ffill')

    # Birleştirilen veriyi Processed_Data klasörüne yeni bir dosya olarak kaydetme
    yeni_dosya_adi = os.path.join(PROCESSED_DIR, f'{hisse_kodu}_final_processed.csv')
    birlestirilmis_data.to_csv(yeni_dosya_adi)
    
    print(f"   ✅ {hisse_kodu} verisi güncellendi ve kaydedildi: {os.path.basename(yeni_dosya_adi)}")

if __name__ == "__main__":
    print("\n--- data_merger_fx.py çalıştı ---")