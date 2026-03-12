import { useState, useEffect, useCallback } from 'react';
import { type Backup, createBackup } from '../models/Backup';

interface UseBackupsResult {
  backups: Backup[];
  loading: boolean;
  error:   string | null;
  reload:  () => void;
}

export function useBackups(): UseBackupsResult {
  const [backups,  setBackups]  = useState<Backup[]>([]);
  const [loading,  setLoading]  = useState<boolean>(true);
  const [error,    setError]    = useState<string | null>(null);
  const [revision, setRevision] = useState<number>(0);

  // Exponer reload como función estable para el consumidor
  const reload = useCallback(() => setRevision(r => r + 1), []);

  useEffect(() => {
    let cancelled = false;

    async function fetchBackups() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/songs_backup');
        if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
        const data: Backup[] = await res.json();
        if (!cancelled) setBackups(data.map(createBackup));
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchBackups();
    return () => { cancelled = true; };
  }, [revision]); // re-ejecuta cuando se llama reload()

  return { backups, loading, error, reload };
}