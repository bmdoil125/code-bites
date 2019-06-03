# services/users/manage.py
import sys
import unittest
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

# instantiate app using Application Factory
app = create_app()
#Extends normal cli with commands related to Flask
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)

@cli.command('add_users')
def add_users():
    """ Adds test users """
    db.session.add(User(username='testuser1', email='testing123@gmail.com'))
    db.session.add(User(username='testuser2', email='testingagain@gmail.com'))
    db.session.commit()


#Instantiate the cli
if __name__ == '__main__':
    cli()