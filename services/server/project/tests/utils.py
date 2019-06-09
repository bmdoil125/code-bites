from project import db
from project.api.models import User, Question, Score

def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user
    
def add_admin_user(username, email, password):
    user = User(username=username, email=email, password=password, admin=True)
    db.session.add(user)
    db.session.commit()
    return user


def add_question(
    author_id=1,
    body=('test'),
    test_code='test',
    test_solution='test',
    difficulty='Easy'):
    question = Question(
        author_id=author_id,
        body=body,
        test_code=test_code,
        test_solution=test_solution,
        difficulty=difficulty
    )

    db.session.add(question)
    db.session.commit()
    return question

def add_score(
    user_id=1,
    question_id=1,
    correct=False,
    points=5,
    runtime=10):
    score = Score(
        user_id=user_id,
        question_id=question_id,
        correct=correct,
        points=points,
        runtime=runtime
    )
    db.session.add(score)
    db.session.commit()
    return score




    