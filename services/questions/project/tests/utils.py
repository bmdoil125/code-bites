from project import db
from project.api.models import Question

def add_question(
    body=('Define a function called sum that takes two integers as '
              'arguments and returns their sum'),
    test_code='sum(2, 2)',
    test_solution='4',
    difficulty='Easy'):
    question = Question(
        body=body,
        test_code=test_code,
        test_solution=test_solution,
        difficulty=difficulty
    )

    db.session.add(question)
    db.session.commit()
    return question
