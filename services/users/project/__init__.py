#  services/users/project/__init__.py
import os
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# instantiate db
db = SQLAlchemy()

#instantiate toolbar
toolbar = DebugToolbarExtension()

#instantiate CORS
cors = CORS()

# instantiate db migrations
migrate = Migrate()

# instantiate password hashing
bcrypt = Bcrypt()

# Application Factory -- instantiate app
def create_app(script_info=None):
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up db extension
    db.init_app(app)
    # set up toolbar extension
    toolbar.init_app(app)
    # set up CORS extension
    cors.init_app(app)
    # set up flask migrate
    migrate.init_app(app, db)
    # set up pass hashing
    bcrypt.init_app(app)
    
    # imported here to avoid circular import
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)
    from project.api.login import login_blueprint
    app.register_blueprint(login_blueprint)

    '''
    shell context for flask cli used to register the app and db to the shell to work with the application context and db
    without having to import directly to shell
    Ex: docker-compose exec users flask shell
    '''
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app



