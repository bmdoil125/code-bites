# services/server/manage.py
import sys
import unittest
import coverage
import random
import string
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User, Question, Score

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

@cli.command('add_test_data')
def add_users():
    # users
    users_num = 100

    # questions
    questions_num = 500
    body_length = 25
    test_code_length = 25
    test_solution_length = 20
    difficulty_levels = ['Easy', 'Moderate', 'Hard']

    # scores
    scores_num = 2000

    """ Add an admin user first """
    db.session.add(User(username='admin', email='admin@admin.com', password='admin', active=True, admin=True))
    db.session.commit()
    
    users_objects = []
    addr = '@example.com'
    for _ in range(0,users_num):
        username = generate_string()
        password = generate_string()
        email = generate_string()
        email += addr
        users_objects.append(User(username=username, email=email, password=password))

    db.session.bulk_save_objects(users_objects)
    db.session.commit()

    questions_objects = []
    for _ in range(0, questions_num):
        author_id = generate_id(users_num)
        body = generate_string(body_length)
        test_code = generate_string(test_code_length)
        test_solution = generate_string(test_solution_length)
        difficulty = random.choice(difficulty_levels)
        questions_objects.append(
            Question(
                author_id=author_id,
                body=body,
                test_code=test_code,
                test_solution=test_solution,
                difficulty=difficulty
            )
        )

    db.session.bulk_save_objects(questions_objects)
    db.session.commit()

    scores_objects = []
    for _ in range(0, scores_num):
        user_id = generate_id(users_num)
        question_id = generate_id(questions_num)
        correct = bool(random.getrandbits(1))
        points = random.randint(1, 10)
        runtime = random.randint(1, 180)

        scores_objects.append(
            Score(
                user_id=user_id,
                question_id=question_id,
                correct=correct,
                points=points,
                runtime=runtime
            )
        )
    
    db.session.bulk_save_objects(scores_objects)
    db.session.commit()
        



def generate_string(size=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(size))

def generate_id(max_id):
    return random.randint(1,max_id)

#Instantiate the cli
if __name__ == '__main__':
    cli()