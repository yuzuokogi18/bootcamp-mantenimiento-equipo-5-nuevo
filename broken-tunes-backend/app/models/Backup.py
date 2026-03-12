from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Backup:
    """
    Representa un backup de la tabla 'songs_backup'.

    Columnas:
        id, original_song_id, title, artist, mp3_data,
        backup_note, backed_up_by, backed_up_at
    """
    id:               int
    title:            str
    artist:           str
    original_song_id: Optional[int]      = None
    mp3_data:         Optional[bytes]    = None
    backup_note:      str                = 'periodic backup'
    backed_up_by:     str                = 'system'
    backed_up_at:     Optional[datetime] = None

    def to_dict(self) -> dict:
        """
        Serializa el backup para respuestas JSON.
        Excluye mp3_data — los bytes se sirven por /play_backup/<id>.
        backed_up_at se convierte a ISO 8601 si es datetime.
        """
        return {
            'id':               self.id,
            'original_song_id': self.original_song_id,
            'title':            self.title,
            'artist':           self.artist,
            'backup_note':      self.backup_note,
            'backed_up_by':     self.backed_up_by,
            'backed_up_at':     (
                self.backed_up_at.isoformat()
                if isinstance(self.backed_up_at, datetime)
                else self.backed_up_at
            ),
        }

    @staticmethod
    def from_row(row: tuple) -> 'Backup':
        """
        Construye un Backup desde una tupla cruda de MySQL.
        Espera el orden:
            (id, original_song_id, title, artist,
             backup_note, backed_up_by, backed_up_at)
        """
        return Backup(
            id=               row[0],
            original_song_id= row[1],
            title=            row[2],
            artist=           row[3],
            backup_note=      row[4] or 'periodic backup',
            backed_up_by=     row[5] or 'system',
            backed_up_at=     row[6],
        )