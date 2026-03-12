from app.repositories.Song_repository import SongRepository
from app.repositories.Backup_repository import BackupRepository

_song_repo   = SongRepository()
_backup_repo = BackupRepository()


class BackupController:
    """
    Lógica de negocio relacionada a backups.
    No importa flask, request ni Response.
    Llama a los repositorios y retorna datos serializables.
    """

    def list_backups(self) -> list[dict]:
        """
        Retorna todos los backups ordenados por fecha descendente.

        Returns:
            list[dict]: Metadata de backups lista para jsonify().
        """
        backups = _backup_repo.get_all()
        return [backup.to_dict() for backup in backups]

    def create_backup(
        self,
        song_id:  int,
        backed_by: str = 'web-ui',
        note:      str = 'manual backup',
    ) -> dict:
        """
        Crea un backup de una canción existente.

        Args:
            song_id:   ID de la canción original a respaldar.
            backed_by: Usuario o sistema que genera el backup.
            note:      Nota descriptiva del backup.

        Returns:
            dict: {'ok': True, 'backup_id': int} si fue exitoso.
                  {'ok': False, 'error': str}    si la canción no existe.
        """
        song = _song_repo.get_by_id(song_id)
        if not song:
            return {'ok': False, 'error': 'song not found'}

        if not song.mp3_data:
            return {'ok': False, 'error': 'song has no audio data'}

        backup_id = _backup_repo.create(song, backed_by, note)
        return {'ok': True, 'backup_id': backup_id}