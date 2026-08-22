'use client';

import { useState, useRef } from 'react';
import { Disc } from 'lucide-react';

export default function AudioPlayer() {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const togglePlay = () => {
    if (!audioRef.current) return;
    
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.volume = 0.4;
      audioRef.current.play().catch(e => console.log("Autoplay bloqueado", e));
    }
    setIsPlaying(!isPlaying);
  };

  return (
    <>
      <audio ref={audioRef} src="/musica.mp3" loop preload="auto" />
      <button 
        onClick={togglePlay}
        className={`fixed bottom-6 right-6 z-50 flex items-center justify-center w-14 h-14 bg-background/90 backdrop-blur-md border border-[#2a2a30] rounded-full shadow-lg hover:border-primary/70 transition-all ${isPlaying ? 'border-primary shadow-[0_0_15px_rgba(200,34,69,0.4)]' : ''}`}
        title={isPlaying ? "Pausar" : "Tocar"}
      >
        <div className={`text-primary flex items-center justify-center ${isPlaying ? 'animate-[spin_4s_linear_infinite]' : ''}`}>
          <Disc size={26} />
        </div>
      </button>
    </>
  );
}

