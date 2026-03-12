from flask import Blueprint, jsonify, Response, abort
from app.controllers.Song_controller import SongController
import app

songs_bp = Blueprint('songs', __name__)
_controller = SongController()


@songs_bp.route('/api/songs', methods=['GET'])
def api_songs():
    try:
        conn = app.get_db()
        cur = conn.cursor()

        cur.execute("SELECT id, title, artist FROM songs")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        songs = [
            {"id": r[0], "title": r[1], "artist": r[2]}
            for r in rows
        ]

        return jsonify(songs)

    except Exception:
        return jsonify([]), 500


@songs_bp.route('/play/<int:song_id>', methods=['GET'])
def play_song(song_id: int):

    result = _controller.stream_song(song_id)

    if not result:
        abort(404)

    mp3_data, filename = result

    return Response(
        mp3_data,
        mimetype="audio/mpeg",
        headers={
            "Content-Disposition": f'inline; filename="{filename}"'
        }
    )