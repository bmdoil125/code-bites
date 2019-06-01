# services/project/config.py
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
class BaseConfig:
    """Base Configuration"""
    TESTING = False
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')

class DevConfig(BaseConfig):
    """Development Configuration"""
    pass

class TestConfig(BaseConfig):
    """Testing Configuration"""
    TESTING = True

class ProdConfig(BaseConfig):
    """Production Configuration"""
    pass