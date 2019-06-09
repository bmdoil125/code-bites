from sqlalchemy.sql import func

from project import db, bcrypt
from flask import current_app, url_for
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


    def __init__(self, username, email, password, active=True, admin=False, questions_authored=[], questions_answered=[]):
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
            'admin': self.admin,
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
                'auth_id': user_id,
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
            return payload['auth_id']
        except jwt.ExpiredSignatureError:
            return 'Please log in again.'
        except jwt.InvalidTokenError:
            return 'Unauthorized'

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # foreign key
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # can't serialize objects, implement backref later
    # https://stackoverflow.com/questions/50226159/object-of-type-product-is-not-json-serializable
    # author = db.relationship("User", back_populates="questions_authored")
    # value = db.relationship("Score", back_populates="question")

    body = db.Column(db.String, nullable=False)
    test_code = db.Column(db.String, nullable=False)
    test_solution = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)


    def __init__(self, author_id, body, test_code, test_solution, difficulty):
        self.author_id = author_id
        self.body = body
        self.test_code = test_code
        self.test_solution = test_solution
        self.difficulty = difficulty

    def to_json(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'body': self.body,
            'test_code': self.test_code,
            'test_solution': self.test_solution,
            'difficulty': self.difficulty,
        }

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

    # Additional parameters
    correct = db.Column(db.Boolean, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, question_id, correct=False, points=1, runtime=0):
        self.user_id = user_id
        self.question_id = question_id
        self.correct = correct
        self.points = points
        self.runtime = runtime

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'correct': self.correct,
            'points': self.points,
            'runtime': self.runtime
        }


