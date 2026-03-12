/**
 * @fileoverview Modelo de datos para una canción.
 * Refleja la respuesta del endpoint GET /api/songs
 */

export interface Song {
  id:     number;
  title:  string;
  artist: string;
}

/**
 * Crea un objeto Song a partir de la respuesta cruda del backend.
 * Normaliza campos faltantes y garantiza la forma del objeto en toda la app.
 */
export function createSong(raw: Song): Song {
  return {
    id:     raw.id,
    title:  raw.title  ?? 'Sin título',
    artist: raw.artist ?? 'Artista desconocido',
  };
}

/**
 * Retorna la URL de reproducción para una canción.
 */
export function getSongPlayUrl(song: Song): string {
  return `/play/${song.id}`;
}