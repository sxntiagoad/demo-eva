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
        """Genera un token personalizado con formato EVA-XXXXXXXXXXXXXXXX"""
        prefix = "EVA"
        random_part = secrets.token_urlsafe(16)[:20]  # Genera 20 caracteres aleatorios
        token = f"{prefix}-{random_part}"
        
        self.token = token
        self.token_expiration = datetime.utcnow() + Config.TOKEN_EXPIRATION
        return token
    
    def is_token_expired(self):
        """
        Verifica si el token ha expirado comparando la fecha actual con token_expiration
        Returns:
            bool: True si el token está expirado o no tiene fecha de expiración,
                  False si el token es válido
        """
        current_time = datetime.utcnow()
        
        # Si no hay fecha de expiración, consideramos el token como expirado
        if not self.token_expiration:
            return True
        
        # Comparamos la fecha actual con la fecha de expiración
        return current_time > self.token_expiration
    
    
    @staticmethod
    def verify_token(token):
        """
        Verifica si un token es válido y no ha expirado
        Args:
            token (str): El token a verificar
        Returns:
            User|None: Retorna el usuario si el token es válido, None si no lo es
        """
        user = User.query.filter_by(token=token).first()
        if not user:
            return None
        
        # Usar el método is_token_expired para la verificación
        if user.is_token_expired():
            return None
        
        return user
    
    @staticmethod
    def find_by_token(token):
        return User.query.filter_by(token=token).first()
    

    def to_dict(self):
        """
        Convierte el usuario a un diccionario para la API
        Incluye información sobre la expiración del token
        """
        current_time = datetime.utcnow()
        return {
            'username': self.username,
            'email': self.email,
            'token': self.token,
            'token_expiration': self.token_expiration.isoformat() if self.token_expiration else None,
            'created_at': self.created_at.isoformat(),
            'current_time': current_time.isoformat()
        }
