# services/project/config.py
import os


class BaseConfig:
    """Base Configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    BASE_URL = os.getenv('BASE_URL')
    DEBUG_TOOLBAR = False
    DEBUG_TOOLBAR_INTERCEPT = False
    BCRYPT_LOG_ROUNDS = 12
    TOKEN_EXPIRATION_DAYS = 5
    TOKEN_EXPIRATION_SECONDS = 0
    PAGINATION_NUMBER = 5

class DevConfig(BaseConfig):
    """Development Configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG_TOOLBAR = True
    BCRYPT_LOG_ROUNDS = 4

class TestConfig(BaseConfig):
    """Testing Configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 5

class ProdConfig(BaseConfig):
    """Production Configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
