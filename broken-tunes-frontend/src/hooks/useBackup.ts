import { useState, useCallback } from 'react';

interface BackupResponse {
  ok:        boolean;
  backup_id: number;
  error?:    string;
}

interface UseBackupResult {
  createBackup: (id: number, note?: string) => Promise<BackupResponse | null>;
  loading:      boolean;
  error:        string | null;
}

export function useBackup(): UseBackupResult {
  const [loading, setLoading] = useState<boolean>(false);
  const [error,   setError]   = useState<string | null>(null);

  const createBackup = useCallback(async (
    id:   number,
    note: string = 'manual backup from UI'
  ): Promise<BackupResponse | null> => {
    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append('backed_by', 'web-ui');
      form.append('note', note);

      const res = await fetch(`/api/backup/${id}`, { method: 'POST', body: form });
      const data: BackupResponse = await res.json();

      if (!res.ok || !data.ok) {
        throw new Error(data.error ?? `Error ${res.status}`);
      }
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createBackup, loading, error };
}