from project.tests.base import BaseTestCase
from project.tests.utils import add_question, add_user

class TestQuestionModel(BaseTestCase):

    def test_add_question(self):
        add_user('test','test','test')
        question = add_question()
        self.assertTrue(question.id)
        self.assertTrue(question.author_id)
        self.assertTrue(question.body)
        self.assertTrue(question.test_code, 'test')
        self.assertTrue(question.test_solution, 'test')
        self.assertTrue(question.difficulty, 'Easy')