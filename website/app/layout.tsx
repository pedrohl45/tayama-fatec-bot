import type { Metadata } from 'next';
import './globals.css';
import AudioPlayer from './components/AudioPlayer';

export const metadata: Metadata = {
  title: 'TayamaBot',
  description: 'Sua assistente acadêmica noturna. Organize sua rotina, acompanhe notas e faça pausas com uma dose de sarcasmo.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&display=swap" rel="stylesheet" />
      </head>
      <body className="font-sans min-h-screen bg-background text-foreground flex flex-col">
        {children}
        <AudioPlayer />
      </body>
    </html>
  );
}

