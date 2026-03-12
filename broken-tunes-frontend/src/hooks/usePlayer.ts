import { useState, useRef, useCallback } from 'react';

interface CurrentSong {
  id:     number;
  title:  string;
  artist: string;
  isBackup: boolean;
}

interface UsePlayerResult {
  audioRef:    React.RefObject<HTMLAudioElement | null>;
  currentSong: CurrentSong | null;
  playbackRate: number;
  play:        (id: number, title?: string, artist?: string) => void;
  playBackup:  (id: number, title?: string, artist?: string) => void;
  setSpeed:    (value: number) => void;
}

export function usePlayer(): UsePlayerResult {
  const audioRef    = useRef<HTMLAudioElement | null>(null);
  const [currentSong,  setCurrentSong]  = useState<CurrentSong | null>(null);
  const [playbackRate, setPlaybackRate] = useState<number>(1.0);

  const applySpeed = useCallback((audio: HTMLAudioElement, rate: number) => {
    audio.playbackRate = rate;
  }, []);

  const play = useCallback((id: number, title = `#${id}`, artist = '—') => {
    const audio = audioRef.current;
    if (!audio) return;

    audio.src = `/play/${id}`;
    applySpeed(audio, playbackRate);
    audio.play().catch(err => console.error('Play error:', err));

    setCurrentSong({ id, title, artist, isBackup: false });
  }, [audioRef, playbackRate, applySpeed]);

  const playBackup = useCallback((id: number, title = `Backup #${id}`, artist = '—') => {
    const audio = audioRef.current;
    if (!audio) return;

    audio.src = `/play_backup/${id}`;
    applySpeed(audio, playbackRate);
    audio.play().catch(err => console.error('PlayBackup error:', err));

    setCurrentSong({ id, title, artist, isBackup: true });
  }, [audioRef, playbackRate, applySpeed]);

  const setSpeed = useCallback((value: number) => {
    const rate  = Math.min(2.0, Math.max(0.5, value)); // clamp 0.5 – 2.0
    const audio = audioRef.current;
    if (audio) applySpeed(audio, rate);
    setPlaybackRate(rate);
  }, [audioRef, applySpeed]);

  return { audioRef, currentSong, playbackRate, play, playBackup, setSpeed };
}