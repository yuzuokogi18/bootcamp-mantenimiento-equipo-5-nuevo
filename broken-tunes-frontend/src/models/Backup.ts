/**
 * @fileoverview Modelo de datos para un backup de canción.
 * Refleja la respuesta del endpoint GET /api/songs_backup
 */

export interface Backup {
  id:               number;
  original_song_id: number;
  title:            string;
  artist:           string;
  backup_note:      string;
  backed_up_by:     string;
  backed_up_at:     string | null;
}

/**
 * Crea un objeto Backup a partir de la respuesta cruda del backend.
 * Normaliza campos faltantes y garantiza la forma del objeto en toda la app.
 */
export function createBackup(raw: Backup): Backup {
  return {
    id:               raw.id,
    original_song_id: raw.original_song_id,
    title:            raw.title       ?? 'Sin título',
    artist:           raw.artist      ?? 'Artista desconocido',
    backup_note:      raw.backup_note ?? '',
    backed_up_by:     raw.backed_up_by ?? 'desconocido',
    backed_up_at:     raw.backed_up_at ?? null,
  };
}

/**
 * Formatea la fecha de backed_up_at para mostrar en la UI.
 * @returns Fecha formateada o '—' si no existe
 * @example formatBackupDate(backup) // "01/06/2024 12:00"
 */
export function formatBackupDate(backup: Backup): string {
  if (!backup.backed_up_at) return '—';
  const date = new Date(backup.backed_up_at);
  return date.toLocaleString('es-ES', {
    day:    '2-digit',
    month:  '2-digit',
    year:   'numeric',
    hour:   '2-digit',
    minute: '2-digit',
  });
}

/**
 * Retorna la URL de reproducción para un backup.
 */
export function getBackupPlayUrl(backup: Backup): string {
  return `/play_backup/${backup.id}`;
}