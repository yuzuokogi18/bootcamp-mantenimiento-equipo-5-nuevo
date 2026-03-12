from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from app.database import get_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    POST /login
    Autentica un usuario por username y password.

    Form data:
        username (str)
        password (str)

    Returns:
        {'ok': True,  'username': str} con status 200 si es válido.
        {'ok': False}                  con status 401 si no es válido.
    """
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, password FROM users WHERE username = %s",
            (username,)
        )
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if row and check_password_hash(row[1], password):
        return jsonify({'ok': True, 'username': username})

    return jsonify({'ok': False}), 401