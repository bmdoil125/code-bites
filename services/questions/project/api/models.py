from project import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String, nullable=False)
    test_code = db.Column(db.String, nullable=False)
    test_solution = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)


    def __init__(self, body, test_code, test_solution, difficulty):
        self.body = body
        self.test_code = test_code
        self.test_solution = test_solution
        self.difficulty = difficulty

    def to_json(self):
        return {
            'id': self.id,
            'body': self.body,
            'test_code': self.test_code,
            'test_solution': self.test_solution,
            'difficulty': self.difficulty
        }