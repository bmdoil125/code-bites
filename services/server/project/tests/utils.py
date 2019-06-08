from project import db
from project.api.models import User, Question

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




    