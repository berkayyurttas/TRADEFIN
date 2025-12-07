// frontend/app/login/page.tsx

import Link from 'next/link';
// Heroicons için React import'u gerekli değildir, ancak kodun doğru yapıda olması önemli.
import { LockClosedIcon, UserIcon } from '@heroicons/react/24/solid'; 
import React from 'react'; // 👈 Bu satır TypeScript ortamında zorunlu olabilir.

const LoginPage = () => {
  return (
    // Ana konteyner
    <div className="flex min-h-screen items-center justify-center bg-bg-dark text-white">
      
      {/* Kart: Formu içeren merkezi kutu */}
      <div className="w-full max-w-md p-8 space-y-8 rounded-xl shadow-2xl bg-card-dark">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-primary-blue">
            TRADEFIN
          </h1>
          <p className="mt-2 text-sm text-gray-400">
            Tahmin Panosuna erişim için giriş yapın
          </p>
        </div>
        
        <form className="mt-8 space-y-6">
          
          {/* Kullanıcı Adı / E-posta Alanı */}
          <div>
            <label htmlFor="email" className="sr-only">E-posta Adresi</label>
            <div className="relative">
              <UserIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500" />
              <input
                id="email"
                name="email"
                type="email"
                required
                className="w-full pl-10 pr-3 py-2 border border-gray-600 placeholder-gray-500 text-white rounded-md focus:outline-none focus:ring-primary-blue focus:border-primary-blue bg-gray-700/50"
                placeholder="E-posta Adresi"
              />
            </div>
          </div>

          {/* Şifre Alanı */}
          <div>
            <label htmlFor="password" className="sr-only">Şifre</label>
            <div className="relative">
              <LockClosedIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500" />
              <input
                id="password"
                name="password"
                type="password"
                required
                className="w-full pl-10 pr-3 py-2 border border-gray-600 placeholder-gray-500 text-white rounded-md focus:outline-none focus:ring-primary-blue focus:border-primary-blue bg-gray-700/50"
                placeholder="Şifre"
              />
            </div>
          </div>

          {/* Giriş Butonu */}
          <div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-blue hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-blue transition duration-150"
            >
              Giriş Yap
            </button>
          </div>
        </form>
        
        {/* Kayıt Ol Linki */}
        <div className="text-sm text-center">
          <p className="text-gray-400">
            Hesabın yok mu?{' '}
            <Link href="/register" className="font-medium text-primary-blue hover:text-blue-400">
              Hemen Kayıt Ol
            </Link>
          </p>
        </div>
        
      </div>
    </div>
  );
};

export default LoginPage;