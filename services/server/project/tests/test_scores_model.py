from project.tests.base import BaseTestCase
from project.tests.utils import add_question, add_user, add_score

class TestScoreModel(BaseTestCase):
    def test_add_score(self):
        add_user('test','test','test')
        add_question()
        score = add_score()
        self.assertTrue(score.id)
        self.assertTrue(score.user_id, 1)
        self.assertTrue(score.question_id, 1)
        self.assertFalse(score.correct)
        self.assertTrue(score.points, 5)
        self.assertTrue(score.runtime, 10)


