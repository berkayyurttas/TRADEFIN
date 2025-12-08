// src/app/page.tsx
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Chart.js'in gerekli bileşenlerini kaydetme
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// Örnek Veri (Bu veriler daha sonra Backend API'den çekilecektir)
const data = {
  labels: ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma'],
  datasets: [
    {
      label: 'GARAN Gerçek Kapanış Fiyatı',
      data: [25.5, 26.1, 25.9, 26.5, 27.2], // Gerçekleşen fiyatlar
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.5)',
      tension: 0.1,
    },
    {
      label: 'Model Tahmini',
      data: [25.7, 26.0, 26.2, 26.4, 27.5], // Modelin yaptığı tahmin
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
      tension: 0.1,
      borderDash: [5, 5], // Kesikli çizgi tahmin olduğunu belirtir
    },
  ],
};

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'GARAN Hisse Fiyatı ve Tahmin',
    },
  },
};

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-start py-8 px-4">
      {/* Başlık */}
      <h1 className="text-4xl font-extrabold text-gray-900 mb-12 mt-8">TRADEFIN 📈</h1>

      {/* Hisse Grafiği Alanı */}
      <div className="w-full max-w-lg bg-white rounded-lg shadow-xl p-6 mb-8 border border-purple-200">
        <h2 className="text-2xl font-semibold text-purple-700 mb-4 text-center">Tahmin Grafiği</h2>
        <div className="mb-4">
          <Line data={data} options={options} />
        </div>
        <p className="text-sm text-gray-500 mt-4 text-center">
            Gerçek fiyat ve yapay zeka modeli tahmininin görselleştirilmesi.
        </p>
      </div>

    </div>
  );
}