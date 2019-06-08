from project.tests.base import BaseTestCase
from project.tests.utils import add_question

class TestQuestionModel(BaseTestCase):

    def test_add_question(self):
        question = add_question()
        self.assertTrue(question.id)
        self.assertTrue(question.body)
        self.assertTrue(question.test_code, 'sum(2, 2)')
        self.assertTrue(question.test_solution, '4')
        self.assertTrue(question.difficulty, 'Easy')