from flask import Flask
from app.database import get_db

app = Flask(__name__)

# registrar rutas
from app.routes import *

__all__ = ["app", "get_db"]