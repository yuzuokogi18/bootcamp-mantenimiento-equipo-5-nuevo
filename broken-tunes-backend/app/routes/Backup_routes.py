from flask import Blueprint, jsonify, request
from app.controllers.Backup_controller import BackupController

backups_bp = Blueprint('backups', __name__)
_controller = BackupController()


@backups_bp.route('/api/songs_backup')
def api_songs_backup():
    """
    GET /api/songs_backup
    Retorna lista de backups ordenados por fecha descendente.
    """
    return jsonify(_controller.list_backups())


@backups_bp.route('/api/backup/<int:song_id>', methods=['POST'])
def api_backup_song(song_id: int):
    """
    POST /api/backup/<song_id>
    Crea un backup de la canción indicada.

    Form data:
        backed_by (str): Usuario que genera el backup. Default: 'web-ui'
        note      (str): Nota descriptiva.            Default: 'manual backup'
    """
    backed_by = request.form.get('backed_by', 'web-ui')
    note      = request.form.get('note', 'manual backup')

    result = _controller.create_backup(song_id, backed_by, note)

    if not result['ok']:
        return jsonify(result), 404

    return jsonify(result)