import json
import unittest

from project import db
from project.tests.base import BaseTestCase
from project.api.models import User

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_User(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])
    
    def test_add_user(self):
        """POST /users add a user"""
        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'brent',
                'email': 'bdoil@brent.com'
            }),
            content_type='application/json',
        )
        # get response data
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)             # test 201 - CREATED
        self.assertIn('bdoil@brent.com', data['message'])       # content contains email
        self.assertIn('success', data['status'])                # return status message
        
    def test_add_user_empty_payload(self):
        """ Throw error if JSON object is empty """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}), # empty payload
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Empty payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_username(self):
        """ Throw error if no username key """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'bdoil@brentdoil.com'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_email(self):
        """ Throw error if no email key """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'username': 'brent'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])
    
    def test_add_user_duplicate_email(self):
        """ Throw error if email already exists """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'brent',
                    'email': 'bdoil@brentdoil.com',
                }),
                content_type='application/json'
                
            )
            # Add duplicate email
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'brent',
                    'email': 'bdoil@brentdoil.com',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_user(self):
        """ Throw error if get single user fails """
        user = User(username='testuser', email='test@testing.io')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('testuser', data['data']['username'])
            self.assertIn('success', data['status'])

                


if __name__ == '__main__':
    unittest.main()