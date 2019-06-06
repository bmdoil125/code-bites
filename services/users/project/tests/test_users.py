import json
import unittest

from project import db
from project.tests.base import BaseTestCase
from project.api.models import User
from project.tests.utils import add_user, add_admin_user


# TODO - Refactor tests to reduce redundancy

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_user(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])
    
    def test_add_user(self):
        """POST /users add a user"""
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
                '/users',
                data=json.dumps({
                    'username': 'brent',
                    'email': 'bdoil@brent.com',
                    'password': 'testpass'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            # get response data
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)             # test 201 - CREATED
            self.assertIn('bdoil@brent.com', data['message'])       # content contains email
            self.assertIn('success', data['status'])                # return status message
        
    def test_add_user_empty_payload(self):
        """ Throw error if JSON object is empty """
        add_admin_user('testuser', 'test@testing.io', 'testpass')
        user = User.query.filter_by(email='test@testing.io').first()
        user.admin = True
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
                '/users',
                data=json.dumps({}), # empty payload
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Empty payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_missing_password(self):
        """ Throw error if no password key """
        add_admin_user('testuser', 'test@testing.io', 'testpass')
        user = User.query.filter_by(email='test@testing.io').first()
        user.admin = True        
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
                '/users',
                data=json.dumps({'username': 'test', 'email': 'bdoil@brentdoil.com'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_username(self):
        """ Throw error if no username key """
        add_admin_user('testuser', 'test@testing.io', 'testpass')
        user = User.query.filter_by(email='test@testing.io').first()
        user.admin = True
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
                '/users',
                data=json.dumps({'email': 'bdoil@brentdoil.com', 'password': 'testpass'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_email(self):
        """ Throw error if no email key """
        add_admin_user('testuser', 'test@testing.io', 'testpass')
        user = User.query.filter_by(email='test@testing.io').first()
        user.admin = True
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
                '/users',
                data=json.dumps({'username': 'brent', 'password': 'testpass'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])
    
    def test_add_user_duplicate_email(self):
        """ Throw error if email already exists """
        add_admin_user('testuser', 'test@testing.io', 'testpass')
        user = User.query.filter_by(email='test@testing.io').first()
        user.admin = True
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
                '/users',
                data=json.dumps({
                    'username': 'brent',
                    'email': 'bdoil@brentdoil.com',
                    'password': 'testpass'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            # Add duplicate email
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'brent',
                    'email': 'bdoil@brentdoil.com',
                    'password': 'testpass'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_user(self):
        """ Throw error if get single user fails """
        user = add_user('testuser', 'test@testing.io', 'testpass')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('testuser', data['data']['username'])
            self.assertIn('success', data['status'])

    def test_get_user_no_id(self):
        """ Error if id not provided """
        with self.client:
            response = self.client.get('/users/fail')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_user_incorrect_id(self):
        """ Error if incorrect id provided """
        with self.client:
            response = self.client.get('/users/1337')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])
                
    def test_get_all_users(self):
        """ Ensure get all users behaves correctly """
        # Add test users
        add_user('testuser1', 'testing123@gmail.com', 'testpass')
        add_user('testuser2', 'testingagain@gmail.com', 'testpass')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('success', data['status'])
            self.assertIn('testuser1', data['data']['users'][0]['username'])
            self.assertIn('testing123@gmail.com', data['data']['users'][0]['email'])
            self.assertTrue(data['data']['users'][0]['active'])
            self.assertFalse(data['data']['users'][0]['admin'])
            self.assertIn('testuser2', data['data']['users'][1]['username'])
            self.assertIn('testingagain@gmail.com', data['data']['users'][1]['email'])
            self.assertTrue(data['data']['users'][1]['active'])
            self.assertFalse(data['data']['users'][1]['admin'])

    def test_index_no_users(self):
        """ Test main route when no users in database: Status 200 """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_index_all_users(self):
        """ Test main route when users exist in database: Status 200 """
        add_user('brent','brent@doil.com', 'testpass')
        add_user('test', 'testing@test.com', 'testpass')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'brent', response.data)
            self.assertIn(b'test', response.data)

    def test_index_add_user(self):
        """ New user can be added via form POST """
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='test', email='testing@gmail.com', password='testpass'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'test', response.data)
    
    def test_add_user_with_inactive_user(self):
        add_admin_user('testuser', 'test@testing.io', 'testpass')
        # update user to inactive
        user = User.query.filter_by(email='test@testing.io').first()
        user.active = False
        db.session.commit()
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
            response = self.client.post('/users',
                data=json.dumps({
                    'username': 'brent',
                    'email': 'brent@brent.com',
                    'password': 'password',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            print(data)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Unauthorized')
            self.assertEqual(response.status_code, 401)

    def test_add_user_without_admin(self):
        add_user('testname', 'test@ing.com', 'testpass')
        with self.client:
            response_login = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@ing.com',
                    'password': 'testpass'
                }),
                content_type='application/json'
            )
            token = json.loads(response_login.data.decode())['token']
            response = self.client.post('/users',
                data=json.dumps({
                    'username': 'brent',
                    'email': 'brent@brent.com',
                    'password': 'password',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            print(data)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Unauthorized')
            self.assertEqual(response.status_code, 401)
    

if __name__ == '__main__':
    unittest.main()