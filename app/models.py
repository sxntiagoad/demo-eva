from app import db
from datetime import datetime, timedelta
import jwt 
from app.config import Config

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
        expiration = datetime.utcnow() + Config.TOKEN_EXPIRATION
        token = jwt.encode(
            {
                'user_id': self.id,
                'exp': expiration,
                'iat': datetime.utcnow()
            },
            Config.SECRET_KEY,
            algorithm='HS256'
        )
        self.token = token
        self.token_expiration = expiration
        return token
