from app import db
from datetime import datetime, timedelta
import jwt
from app.config import Config
import secrets

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    ip_address = db.Column(db.String(20))
    device_info = db.Column(db.String(500))
    token = db.Column(db.String(500), unique=True)
    token_expiration = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_token(self):
        """Genera un token personalizado con formato EVA-XXXXXXXX"""
        prefix = "EVA"
        random_part = secrets.token_urlsafe(6)[:8]  # Genera 8 caracteres aleatorios
        token = f"{prefix}-{random_part}"
        
        self.token = token
        self.token_expiration = datetime.utcnow() + Config.TOKEN_EXPIRATION
        return token
