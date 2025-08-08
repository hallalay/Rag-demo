import './globals.css';
import React from 'react';

export const metadata = { title: 'RAG MVP' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="container mx-auto">{children}</body>
    </html>
  );
}
