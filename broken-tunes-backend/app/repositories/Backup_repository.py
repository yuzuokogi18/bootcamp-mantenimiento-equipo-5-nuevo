from typing import Optional
from app.database import get_db
from app.models.Song import Song
from app.models.Backup import Backup


class BackupRepository:
    """
    Único punto de acceso a datos de la tabla 'songs_backup'.
    Todas las queries relacionadas a backups viven aquí.
    """

    def get_all(self) -> list[Backup]:
        """
        Retorna todos los backups ordenados por fecha descendente.

        Returns:
            list[Backup]: Lista de backups sin mp3_data (solo metadata).
        """
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, original_song_id, title, artist,
                       backup_note, backed_up_by, backed_up_at
                FROM songs_backup
                ORDER BY backed_up_at DESC
            """)
            rows = cur.fetchall()
            return [Backup.from_row(row) for row in rows]
        finally:
            cur.close()
            conn.close()

    def get_by_id(self, backup_id: int) -> Optional[Backup]:
        """
        Busca un backup por ID incluyendo mp3_data para streaming.

        Args:
            backup_id: ID del backup a buscar.

        Returns:
            Backup con mp3_data incluido, o None si no existe.
        """
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, original_song_id, title, artist,
                       backup_note, backed_up_by, backed_up_at, mp3_data
                FROM songs_backup
                WHERE id = %s
            """, (backup_id,))
            row = cur.fetchone()
            if not row:
                return None
            backup = Backup.from_row(row)
            backup.mp3_data = bytes(row[7]) if row[7] else None
            return backup
        finally:
            cur.close()
            conn.close()

    def create(self, song: Song, backed_by: str, note: str) -> int:
        """
        Crea un backup de una canción existente en songs_backup.

        Args:
            song:      Instancia Song con mp3_data incluido.
            backed_by: Usuario o sistema que genera el backup.
            note:      Nota descriptiva del backup.

        Returns:
            int: ID del backup recién creado.
        """
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO songs_backup
                    (original_song_id, title, artist, mp3_data,
                     backup_note, backed_up_by, backed_up_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (song.id, song.title, song.artist,
                  song.mp3_data, note, backed_by))
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()