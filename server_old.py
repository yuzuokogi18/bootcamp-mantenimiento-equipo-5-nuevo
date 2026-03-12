# server_old.py
# Versión anterior del servidor, conservada por compatibilidad y para facilitar pruebas en otro puerto.

from flask import Flask, send_file, abort
from flask_cors import CORS
import mysql.connector
import tempfile
import os

app = Flask(__name__)

# Restringir acceso solo a la app frontend
CORS(app, resources={
    r"/old/*": {"origins": "http://localhost:4200"}
})

DB = {
    'host': 'localhost',
    'user': 'root',              
    'password': '12345',   
    'database': 'broken_tunes'
}

def conn():
    return mysql.connector.connect(**DB)

@app.route('/old/play/<int:sid>')
def old_play(sid):

    if sid <= 0:
        abort(400)

    c = conn()
    cur = c.cursor()

    # CONSULTA SEGURA (evita SQL Injection)
    q = "SELECT id, title, artist, mp3_data FROM songs WHERE id = %s"
    cur.execute(q, (sid,))
    r = cur.fetchone()

    cur.close()
    c.close()

    if not r:
        abort(404)

    # RUTA TEMPORAL COMPATIBLE CON WINDOWS / LINUX
    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, f"old_song_{r[0]}.mp3")

    try:
        with open(filename, 'wb') as f:
            f.write(r[3])

        return send_file(filename, mimetype='audio/mpeg', as_attachment=False)

    except Exception as e:
        return "Error interno del servidor", 500

if __name__ == '__main__':
    app.run(port=5050, debug=True)
