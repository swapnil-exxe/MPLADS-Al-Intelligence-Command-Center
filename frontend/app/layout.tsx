import './globals.css';
import React from 'react';
import { Toaster } from 'sonner';

export const metadata = {
  title: 'MPLADS INTELLIGENCE — MoSPI AI Risk Command Center',
  description: 'AI-powered monitoring of public fund allocation patterns, risk signals, and empirical evidence for MoSPI.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="light">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700;900&display=swap" rel="stylesheet" />
      </head>
      <body className="bg-[#FFFDF5] text-[#000000] min-h-screen selection:bg-[#FFD93D] selection:text-black font-['Space_Grotesk',sans-serif]">
        {children}
        <Toaster position="top-right" richColors theme="light" />
      </body>
    </html>
  );
}
