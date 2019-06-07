# services/users/manage.py
import sys
import unittest
import coverage
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

# instantiate code coverage tests
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)

COV.start()

# instantiate app using Application Factory
app = create_app()
#Extends normal cli with commands related to Flask
cli = FlaskGroup(create_app=create_app)

@cli.command()
def cov():
    """ Coverage tests """
    tests = unittest.TestLoader().discover('project/tests') # find the tests
    result = unittest.TextTestRunner(verbosity=2).run(tests) # run tests
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


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
    db.session.add(User(username='testuser1', email='testing123@gmail.com', password='testpass', active=True, admin=True))
    db.session.add(User(username='testuser2', email='testingagain@gmail.com', password='testpass'))
    db.session.commit()


#Instantiate the cli
if __name__ == '__main__':
    cli()