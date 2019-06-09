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
            self.assertEqual(len(data['data']['scores']), 5)

            # Pagination test
            response = self.client.get(
                '/scores?page=2',
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['scores']), 5)


    def test_get_scores_no_auth_header(self):
        add_user('testuser', 'test@testing.io', 'testpass')
        add_question()
        for _ in range(0,10):
            add_score()

        with self.client:
            self.client.post(
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
        add_user('testuser', 'test@testing.io', 'testpass')
        add_user('test', 'test', 'test')
        add_question()
        for _ in range(0,5):
            add_score()

        for _ in range(0,5):
            add_score(user_id=2)

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
                '/scores/user',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['scores']), 5)
            self.assertTrue(data['data']['scores'][0]['self'])


    def test_get_user_score(self):
        """ Ensure get authenticated user score works """
        user = add_user('testuser', 'test@testing.io', 'testpass')
        add_question()
        score = add_score()
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
                f'/scores/{score.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['data']['user_id'], 1)
            self.assertEqual(data['data']['question_id'], 1)
            self.assertFalse(data['data']['correct'])
            self.assertEqual(data['data']['points'], 5)
            self.assertEqual(data['data']['runtime'], 10)

    def test_get_user_score_noauth(self):
        """ Ensure fails with 401 unauthorized """
        user = add_user('testuser', 'test@testing.io', 'testpass')
        add_question()
        score = add_score()
        with self.client:
            response = self.client.get(
                f'/scores/{score.id}/user/{user.id}',
                headers={'Authorization': f'Bearer fail'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn('fail', data['status'])
            self.assertIn('Unauthorized', data['message'])


    def test_get_user_score_incorrect_user(self):
        """ Ensure get wrong user score fails with 403 """
        add_user('testuser', 'test@testing.io', 'testpass')
        add_question()
        score = add_score()       
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
                f'/scores/{score.id}/user/999',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('fail', data['status'])
            self.assertIn('You do not have permission to view this score', data['message'])

    def test_update_user_score(self):
        user = add_user('testuser', 'test@testing.io', 'testpass')
        add_question()
        score = add_score()
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
            get_response = self.client.get(
                f'/scores/{score.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertEqual(data['data']['user_id'], 1)
            self.assertEqual(data['data']['question_id'], 1)
            self.assertFalse(data['data']['correct'])
            self.assertEqual(data['data']['points'], 5)
            self.assertEqual(data['data']['runtime'], 10)       

            put_response = self.client.put(
                f'/scores/{score.id}/user/{user.id}',
                data=json.dumps({'correct': False, 'runtime': 15}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}                
            )
            put_data = json.loads(put_response.data.decode())
            self.assertEqual(put_response.status_code, 201)
            self.assertEqual(put_data['data']['user_id'], 1)
            self.assertEqual(put_data['data']['question_id'], 1)
            self.assertFalse(put_data['data']['correct'])
            self.assertEqual(put_data['data']['points'], 5)
            self.assertEqual(put_data['data']['runtime'], 15)

    def test_update_user_score_unauthorized(self):
        # user_id = 1
        user = add_user('testuser', 'test@testing.io', 'testpass')
        # user_id = 2
        user_2 = add_user('test', 'test', 'test')
        add_question(1)
        add_question(2)
        score = add_score(1)
        score_2 = add_score(2)

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
            get_response = self.client.get(
                f'/scores/{score.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertEqual(data['data']['user_id'], 1)
            self.assertEqual(data['data']['question_id'], 1)
            self.assertFalse(data['data']['correct'])
            self.assertEqual(data['data']['points'], 5)
            self.assertEqual(data['data']['runtime'], 10)

            put_response = self.client.put(
                f'/scores/{score_2.id}/user/{user_2.id}',
                data=json.dumps({'correct': False, 'runtime': 15}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}                
            )
            put_data = json.loads(put_response.data.decode())
            self.assertEqual(put_response.status_code, 403)
            self.assertIn('fail', put_data['status'])
            self.assertIn('You do not have permission to update this score', put_data['message'])

    def test_delete_user_score(self):
        # user_id = 1
        user = add_user('testuser', 'test@testing.io', 'testpass')
        add_question()
        score = add_score()
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
            get_response = self.client.get(
                f'/scores/{score.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertEqual(data['data']['user_id'], 1)
            self.assertEqual(data['data']['question_id'], 1)

            delete_response = self.client.delete(
                f'/scores/{score.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            # print(delete_response)
            self.assertEqual(delete_response.status_code, 204)

    def test_delete_user_score_unauthorized(self):
        # user_id = 1
        user = add_user('testuser', 'test@testing.io', 'testpass')
        # user_id = 2
        user_2 = add_user('test', 'test', 'test')

        add_question(1)
        add_question(2)
        score = add_score(1)
        score_2 = add_score(2)

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
            get_response = self.client.get(
                f'/scores/{score.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertEqual(data['data']['user_id'], 1)
            self.assertEqual(data['data']['question_id'], 1)
            self.assertFalse(data['data']['correct'])
            self.assertEqual(data['data']['points'], 5)
            self.assertEqual(data['data']['runtime'], 10)

            delete_response = self.client.delete(
                f'/scores/{score_2.id}/user/{user_2.id}',
                data=json.dumps({'correct': False, 'runtime': 15}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}                
            )
            delete_data = json.loads(delete_response.data.decode())
            self.assertEqual(delete_response.status_code, 403)
            self.assertIn('fail', delete_data['status'])
            self.assertIn('You do not have permission to delete this score', delete_data['message'])


    