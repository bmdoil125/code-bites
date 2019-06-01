# services/users/manage.py

from flask.cli import FlaskGroup
from project import app

#Extends normal cli with commands related to Flask
cli = FlaskGroup(app)

#Instantiate the cli
if __name__ == '__main__':
    cli()