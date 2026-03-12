
# Song model for songs view
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Song:
    """
    Representa una canción de la VIEW 'songs'.
    La VIEW une songs_data + artists, por eso artist es string y no FK.

    Columnas de la VIEW:
        songs_data.id, songs_data.title, artists.name AS artist,
        songs_data.mp3_data, songs_data.created_at
    """
    id:         int
    title:      str
    artist:     str
    mp3_data:   Optional[bytes] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """
        Serializa la canción para respuestas JSON.
        Excluye mp3_data — los bytes de audio se sirven por /play/<id>.
        """
        return {
            'id':         self.id,
            'title':      self.title,
            'artist':     self.artist,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def from_row(row: tuple) -> 'Song':
        """
        Construye un Song desde una tupla cruda de MySQL.
        Espera el orden: (id, title, artist, mp3_data, created_at)
        """
        return Song(
            id=row[0],
            title=row[1],
            artist=row[2],
            mp3_data=bytes(row[3]) if row[3] else None,
            created_at=row[4] if len(row) > 4 else None,
        )