import os
from dotenv import load_dotenv
from flask import Flask

from app.routes.Song_routes   import songs_bp
from app.routes.Backup_routes import backups_bp
from app.routes.Auth_routes   import auth_bp

load_dotenv()

app = Flask(__name__)

app.register_blueprint(songs_bp)
app.register_blueprint(backups_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)