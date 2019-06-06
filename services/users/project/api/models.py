from sqlalchemy.sql import func

from project import db, bcrypt
from flask import current_app
import jwt
import datetime

class User(db.Model):  
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, username, email, password, active=True, admin=False):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode(),
        self.active = active
        self.admin = admin

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'admin': self.admin
        }
    
    def encode_jwt(self, user_id):
        """ Generate JWT """
        try: 
            # JWT Claims http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html#RegisteredClaimName
            payload = { 
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS'),
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    # static methods can be called on a class or an instance        
    @staticmethod
    def decode_jwt(token):
        """ Decode JWT """
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Please log in again.'
        except jwt.InvalidTokenError:
            return 'Unauthorized'
