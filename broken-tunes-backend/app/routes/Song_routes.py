from flask import Blueprint, jsonify, Response, abort
from app.controllers.Song_controller import SongController

songs_bp = Blueprint('songs', __name__)
_controller = SongController()


@songs_bp.route('/api/songs')
def api_songs():
    """
    GET /api/songs
    Retorna lista de canciones con audio válido.
    """
    return jsonify(_controller.list_songs())


@songs_bp.route('/play/<int:song_id>')
def play_song(song_id: int):
    """
    GET /play/<song_id>
    Sirve el audio MP3 de una canción para streaming.
    """
    result = _controller.stream_song(song_id)
    if not result:
        abort(404)

    mp3_data, filename = result
    return Response(
        mp3_data,
        mimetype='audio/mpeg',
        headers={
            'Content-Disposition': f'inline; filename="{filename}"'
        }
    )