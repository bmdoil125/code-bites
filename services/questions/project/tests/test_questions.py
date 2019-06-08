import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_question

class TestQuestionsService(BaseTestCase):
    """ Tests for the Questions Service. """

    def test_all_questions(self):
        add_question()
        add_question('Testing', 'print("Testing")', 'Testing', 'Easy')

        with self.client:
            response = self.client.get('/questions')
            data = json.loads(response.data.decode())