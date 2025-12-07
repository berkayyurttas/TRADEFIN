// frontend/app/page.tsx

import { redirect } from 'next/navigation';

export default function Home() {
  // Varsayılan kodu sildik ve kullanıcıyı Login sayfasına yönlendiriyoruz.
  redirect('/login');
}