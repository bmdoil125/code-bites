import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_question, add_admin_user, add_user

class TestQuestions(BaseTestCase):
    """ Tests for the Questions API. """
    def test_add_question(self):
        """ Ensure a new question can be added to the database """

        # Must be authenticated to add question
        add_user('testuser', 'test@testing.io', 'testpass')
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
                '/questions',
                data=json.dumps({
                    'author_id': 1,
                    'body': 'Sample question',
                    'test_code': 'testing',
                    'test_solution': 'still testing',
                    'difficulty': 'Moderate',
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Question added', data['message'])
            self.assertIn('success', data['status'])
            
    def test_add_question_invalid_keys(self):
        """ Error thrown if invalid JSON object """
        add_admin_user('testuser', 'test@testing.io', 'testpass')
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
                '/questions',
                data=json.dumps({'body':'test'}),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_question_duplicate(self):
        """ Allow duplicate questions """
        add_user('testuser', 'test@testing.io', 'testpass')
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
                '/questions',
                data=json.dumps({
                    'author_id': 1,
                    'body': 'Sample question',
                    'test_code': 'testing',
                    'test_solution': 'still testing',
                    'difficulty': 'Moderate',
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )

            response = self.client.post(
                '/questions',
                data=json.dumps({
                    'author_id': 1,
                    'body': 'Sample question',
                    'test_code': 'testing',
                    'test_solution': 'still testing',
                    'difficulty': 'Moderate',
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Question added', data['message'])
            self.assertIn('success', data['status'])


    def test_add_question_no_auth(self):
        """ Error thrown if no Auth header """
        with self.client:
            response = self.client.post(
                '/questions',
                data=json.dumps({
                    'author_id': 1,
                    'body':'test',
                    'test_code': 'test',
                    'test_solution': 'test',
                    'difficulty': 'easy',
                    }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('Forbidden', data['message'])
            self.assertIn('fail', data['status'])


    def test_add_question_admin(self):
        """ Ensure a new question can be added to the database """

        # Must be authenticated to add question
        add_admin_user('testuser', 'test@testing.io', 'testpass')
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
                '/questions',
                data=json.dumps({
                    'author_id': 1,
                    'body': 'Sample question',
                    'test_code': 'testing',
                    'test_solution': 'still testing',
                    'difficulty': 'Moderate',
                }),
                content_type='application/json',
                headers=({'Authorization': f'Bearer {token}'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Question added', data['message'])
            self.assertIn('success', data['status'])

    def test_get_all_questions(self):
        """ Ensure getting all questions is working for admin"""
        # By default this user will have id=1. At least 1 user is required to add questions
        add_admin_user('testuser', 'test@testing.io', 'testpass')
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


            # author_id = 1 
            add_question()
            add_question(1,'Testing', '# print("Testing")', 'Testing', 'Easy')


            response = self.client.get(
                '/questions',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['questions']), 2)
            self.assertIn(
                'test',
                data['data']['questions'][0]['body'])
            self.assertIn(
                'test',
                data['data']['questions'][0]['test_code']
            )
            self.assertIn(
                'Testing',
                data['data']['questions'][1]['body']
            )
            self.assertIn(
                '# print("Testing")',
                data['data']['questions'][1]['test_code']
            )
            self.assertIn(
                'Testing',
                data['data']['questions'][1]['test_solution']
            )
            self.assertIn(
                'Easy',
                data['data']['questions'][1]['difficulty']
            )

    def test_get_user_questions_list_authenticated(self):
        # user_id = 1
        add_user('testuser', 'test@testing.io', 'testpass')
        # user_id = 2
        add_user('dontshowme', 'dontshowme', 'testpass')
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
            # author_id = 1 
            add_question()
            add_question(1,'Testing', '# print("Testing")', 'Testing', 'Easy')
            add_question(2,'Testing', '# print("Testing")', 'Testing', 'Easy')

            response = self.client.get(
                '/questions/user',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['questions']), 2)
            self.assertIn(
                'test',
                data['data']['questions'][0]['body'])
            self.assertIn(
                'test',
                data['data']['questions'][0]['test_code']
            )
            self.assertIn(
                'Testing',
                data['data']['questions'][1]['body']
            )
            self.assertIn(
                '# print("Testing")',
                data['data']['questions'][1]['test_code']
            )
            self.assertIn(
                'Testing',
                data['data']['questions'][1]['test_solution']
            )
            self.assertIn(
                'Easy',
                data['data']['questions'][1]['difficulty']
            )


    def test_get_user_question(self):
        """ Ensure get authenticated user question works """
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

            response = self.client.get(
                f'/questions/{question.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('test', data['data']['body'])
            self.assertIn('test', data['data']['test_code'])

    def test_get_user_question_noauth(self):
        """ Ensure fails with 401 unauthorized """
        user = add_user('testuser', 'test@testing.io', 'testpass')
        question = add_question()
        with self.client:
            response = self.client.get(
                f'/questions/{question.id}/user/{user.id}',
                headers={'Authorization': 'Bearer fail'}   
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn('fail', data['status'])
            self.assertIn('Unauthorized', data['message'])


    def test_get_user_question_incorrect_user(self):
        """ Ensure get wrong user question fails with 403 """
        add_user('testuser', 'test@testing.io', 'testpass')
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

            response = self.client.get(
                f'/questions/{question.id}/user/999',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('fail', data['status'])
            self.assertIn('You do not have permission to view this question', data['message'])

    def test_update_user_question(self):
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
            get_response = self.client.get(
                f'/questions/{question.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('test', data['data']['body'])
            self.assertIn('test', data['data']['test_code'])

            put_response = self.client.put(
                f'/questions/{question.id}/user/{user.id}',
                data=json.dumps({'body': 'updatedquestionhere'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}                
            )

            put_data = json.loads(put_response.data.decode())
            self.assertEqual(put_response.status_code, 201)
            self.assertIn('updatedquestionhere', put_data['data']['body'])
            self.assertIn('success', put_data['status'])


    def test_update_user_question_unauthorized(self):
        # user_id = 1
        user = add_user('testuser', 'test@testing.io', 'testpass')
        # user_id = 2
        user_2 = add_user('test', 'test', 'test')

        # author_id = 1
        question = add_question()

        # author_id = 2
        question_2 = add_question(2)

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
                f'/questions/{question.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('test', data['data']['body'])
            self.assertIn('test', data['data']['test_code'])

            put_response = self.client.put(
                f'/questions/{question_2.id}/user/{user_2.id}',
                data=json.dumps({'body': 'updatedquestionhere'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}                
            )

            put_data = json.loads(put_response.data.decode())
            self.assertEqual(put_response.status_code, 403)
            self.assertIn('fail', put_data['status'])
            self.assertIn('You do not have permission to update this question', put_data['message'])


    def test_delete_user_question(self):
        # user_id = 1
        user = add_user('testuser', 'test@testing.io', 'testpass')
        # author_id = 1
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
            get_response = self.client.get(
                f'/questions/{question.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('test', data['data']['body'])
            self.assertIn('test', data['data']['test_code'])

            delete_response = self.client.delete(
                f'/questions/{question.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            # print(delete_response)
            self.assertEqual(delete_response.status_code, 204)


    def test_delete_user_question_unauthorized(self):
        # user_id = 1
        user = add_user('testuser', 'test@testing.io', 'testpass')
        # user_id = 2
        user_2 = add_user('test', 'test', 'test')

        # author_id = 1
        question = add_question()

        # author_id = 2
        question_2 = add_question(2)

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
                f'/questions/{question.id}/user/{user.id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('test', data['data']['body'])
            self.assertIn('test', data['data']['test_code'])

            delete_response = self.client.delete(
                f'/questions/{question_2.id}/user/{user_2.id}',
                data=json.dumps({'body': 'updatedquestionhere'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}                
            )
            data = json.loads(delete_response.data.decode())
            self.assertEqual(delete_response.status_code, 403)
            self.assertIn('fail', data['status'])
            self.assertIn('You do not have permission to delete this question', data['message'])


if __name__ == '__main__':
    unittest.main()