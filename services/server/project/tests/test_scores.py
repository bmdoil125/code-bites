import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_question, add_admin_user, add_user, add_score

class TestScores(BaseTestCase):
    """ Tests for the Scores API """
    def test_add_score(self):
        """ Ensure a new score can be added to the database """

        # Must be authenticated to add score
        user = add_user('testuser', 'test@testing.io', 'testpass')
        question = add_question()
        with self.client:
            response_login = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@testing.io',
                    'password': 'testpass'
                }),
                content_type='application/json'                
            )
            token = json.loads(response_login.data.decode())['token']

            response = self.client.post(
                '/scores',
                data=json.dumps({
                    'user_id': user.id,
                    'question_id': question.id,
                    'correct': True,
                    'points': 2,
                    'runtime': 5
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Score added', data['message'])
            self.assertIn('success', data['status'])


    def test_add_score_invalid_keys(self):
        """ Error thrown if invalid JSON object """
        # Must be authenticated to add score
        user = add_user('testuser', 'test@testing.io', 'testpass')
        question = add_question()
        with self.client:
            response_login = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@testing.io',
                    'password': 'testpass'
                }),
                content_type='application/json'                
            )
            token = json.loads(response_login.data.decode())['token']

            response = self.client.post(
                '/scores',
                data=json.dumps({
                    'user_id': user.id,
                    'question_id': question.id,
                    'correct': True,
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])


    def test_add_score_duplicate(self):
        """ Allow duplicate scores """
        # Must be authenticated to add score
        user = add_user('testuser', 'test@testing.io', 'testpass')
        question = add_question()
        with self.client:
            response_login = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@testing.io',
                    'password': 'testpass'
                }),
                content_type='application/json'                
            )
            token = json.loads(response_login.data.decode())['token']

            self.client.post(
                '/scores',
                data=json.dumps({
                    'user_id': user.id,
                    'question_id': question.id,
                    'correct': True,
                    'points': 2,
                    'runtime': 5
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )

            response = self.client.post(
                '/scores',
                data=json.dumps({
                    'user_id': user.id,
                    'question_id': question.id,
                    'correct': True,
                    'points': 2,
                    'runtime': 5
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Score added', data['message'])
            self.assertIn('success', data['status'])

    def test_add_score_no_auth(self):
        """ Error thrown if no Auth header """
        user = add_user('testuser', 'test@testing.io', 'testpass')
        question = add_question()
        with self.client:
            response = self.client.post(
                '/scores',
                data=json.dumps({
                    'user_id': user.id,
                    'question_id': question.id,
                    'correct': True,
                    'points': 2,
                    'runtime': 5
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('Forbidden', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_score_admin(self):
        """ Ensure a new question can be added to the database """
        user = add_admin_user('testuser', 'test@testing.io', 'testpass')
        question = add_question()
        with self.client:
            response_login = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@testing.io',
                    'password': 'testpass'
                }),
                content_type='application/json'                
            )
            token = json.loads(response_login.data.decode())['token']

            response = self.client.post(
                '/scores',
                data=json.dumps({
                    'user_id': user.id,
                    'question_id': question.id,
                    'correct': True,
                    'points': 2,
                    'runtime': 5
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Score added', data['message'])
            self.assertIn('success', data['status'])


    def test_add_score_no_content_header(self):
        """ Ensure a new question can be added to the database """
        user = add_admin_user('testuser', 'test@testing.io', 'testpass')
        question = add_question()
        with self.client:
            response_login = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@testing.io',
                    'password': 'testpass'
                }),
                content_type='application/json'                
            )
            token = json.loads(response_login.data.decode())['token']

            response = self.client.post(
                '/scores',
                data=json.dumps({
                    'user_id': user.id,
                    'question_id': question.id,
                    'correct': True,
                    'points': 2,
                    'runtime': 5
                }),
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 406)
            self.assertIn('This endpoint only accepts json', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_all_scores(self):
        """ Ensure getting all questions is working for admin"""
        # Must be authenticated to add score
        add_user('testuser', 'test@testing.io', 'testpass')
        add_question()
        for _ in range(0,10):
            add_score()

        with self.client:
            response_login = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@testing.io',
                    'password': 'testpass'
                }),
                content_type='application/json'                
            )
            token = json.loads(response_login.data.decode())['token']

            response = self.client.get(
                '/scores',
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['scores']), 10)


    def test_get_scores_no_auth_header(self):
        add_user('testuser', 'test@testing.io', 'testpass')
        add_question()
        for _ in range(0,10):
            add_score()

        with self.client:
            response_login = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@testing.io',
                    'password': 'testpass'
                }),
                content_type='application/json'                
            )

            response = self.client.get(
                '/scores',
                content_type='application/json',
            )
            data = json.loads(response.data.decode()) 
            self.assertEqual(response.status_code, 403)
            self.assertIn('fail', data['status'])      


    def test_get_user_scores_list_authenticated(self):
        pass

    def test_get_user_score(self):
        """ Ensure get authenticated user score works """
        pass

    def test_get_user_score_noauth(self):
        """ Ensure fails with 401 unauthorized """
        pass

    def test_get_user_score_incorrect_user(self):
        """ Ensure get wrong user score fails with 403 """
        pass

    def test_update_user_score(self):
        pass


    def test_update_user_score_unauthorized(self):
        pass

    def test_delete_user_score(self):
        pass

    def test_delete_user_score_unauthorized(self):
        pass


    