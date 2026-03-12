from typing import Optional
from app.database import get_db
from app.models.Song import Song


class SongRepository:
    """
    Único punto de acceso a datos de la tabla/view 'songs'.
    Todas las queries relacionadas a canciones viven aquí.
    """

    def get_all(self) -> list[Song]:
        """
        Retorna todas las canciones que tienen audio válido.
        Replica el FIX BUG #14: filtra mp3_data nulo o muy corto.

        Returns:
            list[Song]: Lista de canciones sin mp3_data (solo metadata).
        """
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, artist, mp3_data, created_at
                FROM songs
                WHERE mp3_data IS NOT NULL
                  AND LENGTH(mp3_data) > 10
            """)
            rows = cur.fetchall()
            return [Song.from_row(row) for row in rows]
        finally:
            cur.close()
            conn.close()

    def get_by_id(self, song_id: int) -> Optional[Song]:
        """
        Busca una canción por ID incluyendo mp3_data para streaming.

        Args:
            song_id: ID de la canción a buscar.

        Returns:
            Song con mp3_data incluido, o None si no existe.
        """
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, artist, mp3_data, created_at
                FROM songs
                WHERE id = %s
            """, (song_id,))
            row = cur.fetchone()
            return Song.from_row(row) if row else None
        finally:
            cur.close()
            conn.close()