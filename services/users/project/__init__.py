#services/users/project/__init__.py

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os

#instantiate db
db = SQLAlchemy()

#Application Factory -- instantiate app
def create_app(script_info=None):
    app = Flask(__name__)

    #set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    #set up db extension
    db.init_app(app)

    #imported here to avoid circular import
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    '''
    shell context for flask cli used to register the app and db to the shell to work with the application context and db 
    without having to import directly to shell
    Ex: docker-compose exec users flask shell
    ''' 
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app




