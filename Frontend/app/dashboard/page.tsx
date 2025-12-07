// frontend/app/dashboard/page.tsx
// Kontrol Paneli (Dashboard) Ana Düzeni

import React from 'react';
import HeaderFX from '@/src/components/HeaderFX'; // 👈 HeaderFX bileşenini içe aktar!
// Bu import'un çalışması için 'frontend/src/components/HeaderFX.tsx' dosyasının var olması gerekir.

// Sol kenar çubuğu genişliği
const SIDEBAR_WIDTH = '250px';

const DashboardPage = () => {
  return (
    // Ana konteyner: Tüm sayfayı kaplar ve koyu arka planı uygular
    <div className="flex min-h-screen bg-bg-dark text-white">

      {/* 1. Sol Kenar Çubuğu (Sidebar) */}
      <nav
        className="fixed top-0 left-0 h-screen bg-card-dark shadow-xl border-r border-gray-700 p-4 flex flex-col z-10"
        style={{ width: SIDEBAR_WIDTH }}
      >
        <div className="text-2xl font-bold text-primary-blue mb-8">
          TRADEFIN Dashboard
        </div>
        
        {/* Navigasyon Elemanları Placeholder */}
        <ul className="space-y-4 text-gray-400">
          <li className="p-2 hover:bg-gray-700 rounded transition duration-150 cursor-pointer">
            Tahminler
          </li>
          <li className="p-2 hover:bg-gray-700 rounded transition duration-150 cursor-pointer">
            Kurlar (2027 Projeksiyon)
          </li>
          <li className="p-2 hover:bg-gray-700 rounded transition duration-150 cursor-pointer">
            Ayarlar
          </li>
        </ul>
      </nav>

      {/* 2. Ana İçerik Alanı */}
      <main 
        className="flex-1 flex flex-col"
        style={{ marginLeft: SIDEBAR_WIDTH }} // Sidebar kadar boşluk bırakır
      >
        
        {/* Üst Çubuk (Header): Anlık Kur Bilgileri Burada Gösterilecektir */}
        <header className="w-full bg-card-dark/50 border-b border-gray-700 p-4 flex justify-between items-center sticky top-0 z-0">
          <h1 className="text-xl font-semibold text-gray-300">
            Pano Genel Bakış
          </h1>
          
          {/* HeaderFX Widget'ını buraya ekliyoruz */}
          <HeaderFX /> {/* 👈 DEĞİŞİKLİK BURADA */}
          
        </header>

        {/* Dashboard Widget Alanı */}
        <div className="p-6 space-y-6">
          <h2 className="text-2xl font-bold text-gray-200 mb-4">
            Hoş Geldiniz!
          </h2>
          
          {/* Widget Grid Alanı Placeholder */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="p-6 bg-card-dark rounded-xl border border-gray-700 shadow-lg h-60">
              Hisse Grafiği Widget'ı
            </div>
            <div className="p-6 bg-card-dark rounded-xl border border-gray-700 shadow-lg h-60">
              Tahmin Kutusu Widget'ı
            </div>
            <div className="p-6 bg-card-dark rounded-xl border border-gray-700 shadow-lg h-60 col-span-full">
              Uzun Vadeli Kur Projeksiyon Grafiği
            </div>
          </div>
        </div>
        
      </main>
    </div>
  );
};

export default DashboardPage;