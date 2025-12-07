// frontend/tailwind.config.ts

import type { Config } from 'tailwindcss';

const config: Config = {
  // 👇 BURASI ÖNEMLİ: Tüm proje dosyalarını taradığından emin olun
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}', // src klasörünü de kapsıyor olmalı
  ],
  darkMode: 'class', // Koyu temayı etkinleştirir
  theme: {
    extend: {
      colors: {
        'primary-blue': '#1a73e8', // Ana renk
        'financial-green': '#16a34a', // Yeşil (Yükseliş)
        'financial-red': '#dc2626', // Kırmızı (Düşüş)
        'bg-dark': '#121212', // Ana arka plan
        'card-dark': '#1e1e1e', // Kart arka planları
      },
    },
  },
  plugins: [],
};

export default config;