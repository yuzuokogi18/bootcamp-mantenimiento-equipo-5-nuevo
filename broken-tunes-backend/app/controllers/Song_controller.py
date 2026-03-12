from typing import Optional
from app.repositories.Song_repository import SongRepository

_repo = SongRepository()


class SongController:
    """
    Lógica de negocio relacionada a canciones.
    No importa flask, request ni Response.
    Llama al repositorio y retorna datos serializables.
    """

    def list_songs(self) -> list[dict]:
        """
        Retorna todas las canciones con audio válido como lista de dicts.

        Returns:
            list[dict]: Metadata de canciones lista para jsonify().
        """
        songs = _repo.get_all()
        return [song.to_dict() for song in songs]

    def stream_song(self, song_id: int) -> Optional[tuple[bytes, str]]:
        """
        Obtiene los bytes de audio y el nombre de archivo de una canción.

        Args:
            song_id: ID de la canción a reproducir.

        Returns:
            tuple[bytes, str]: (mp3_data, filename) si existe.
            None si la canción no existe o no tiene audio.
        """
        song = _repo.get_by_id(song_id)
        if not song or not song.mp3_data:
            return None
        filename = f"{song.title}.mp3"
        return song.mp3_data, filename