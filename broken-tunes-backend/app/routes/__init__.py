from app import app

from app.routes.Song_routes import songs_bp
from app.routes.Backup_routes import backups_bp
from app.routes.Auth_routes import auth_bp

app.register_blueprint(songs_bp)
app.register_blueprint(backups_bp)
app.register_blueprint(auth_bp)