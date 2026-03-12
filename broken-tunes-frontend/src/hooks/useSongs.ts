import { useState, useEffect } from 'react';
import type { Song } from '../models/Song';
import { createSong } from '../models/Song';

interface UseSongsResult {
  songs:   Song[];
  loading: boolean;
  error:   string | null;
}

export function useSongs(): UseSongsResult {
  const [songs,   setSongs]   = useState<Song[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error,   setError]   = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchSongs() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/songs');
        if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
        const data: Song[] = await res.json();
        if (!cancelled) setSongs(data.map(createSong));
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchSongs();
    return () => { cancelled = true; };
  }, []);

  return { songs, loading, error };
}