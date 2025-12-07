// frontend/app/dashboard/page.tsx
// HeaderFX import'unun doğru olduğunu kontrol edin

import React from 'react';
import HeaderFX from '@/src/components/HeaderFX'; // <-- Kırmızı uyarı verse bile, rota doğru olmalı

// Sol kenar çubuğu genişliği
const SIDEBAR_WIDTH = '250px';

const DashboardPage = () => {
  return (
    // Ana konteyner: min-h-screen ve koyu tema sınıfları kesinlikle olmalı
    <div className="flex min-h-screen bg-bg-dark text-white"> 

      {/* 1. Sol Kenar Çubuğu (Sidebar) */}
      <nav
        // Sidebar'ı sabitler ve koyu kart temasını uygular
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
          {/* ... Diğer navigasyon elemanları */}
        </ul>
      </nav>

      {/* 2. Ana İçerik Alanı */}
      <main 
        className="flex-1 flex flex-col"
        style={{ marginLeft: SIDEBAR_WIDTH }}
      >
        
        {/* Üst Çubuk (Header) */}
        <header className="w-full bg-card-dark/50 border-b border-gray-700 p-4 flex justify-between items-center sticky top-0 z-0">
          <h1 className="text-xl font-semibold text-gray-300">
            Pano Genel Bakış
          </h1>
          <HeaderFX />
        </header>

        {/* ... (Widget Alanı) */}
        
      </main>
    </div>
  );
};

export default DashboardPage;