// frontend/app/dashboard/layout.tsx

// frontend/app/layout.tsx

// ...
// import "./globals.css"; // BU SATIRI YORUM SATIRI YAPIN VEYA SİLİN
// ...

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // ...
    // Koyu temayı zorla
    <html lang="tr" className="dark"> 
      <body>{children}</body>
    </html>
  );
}
