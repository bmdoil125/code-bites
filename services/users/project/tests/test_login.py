import json
import unittest

from project import db
from project.tests.base import BaseTestCase
from project.api.models import User
from project.tests.utils import add_user



class TestLoginRoute(BaseTestCase):
    def test_user_reg(self):
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_correct),
                content_type = 'application/json'
            )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Registered')
        self.assertTrue(response.content_type == 'application/json')
        self.assertTrue(response.status_code, 201)
        self.assertTrue(data['token'])
    
    def test_user_reg_empty_payload(self):
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps({}),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Empty payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_reg_html_content(self):
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_correct),
                content_type = 'text/html'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid header: Content-Type', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_reg_invalid_username(self):
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_no_username),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])


    def test_user_reg_invalid_email(self):
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_no_email),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_reg_missing_password(self):
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_no_pass),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_reg_duplicate_email(self):
        """ Throw error if email already exists """
        add_user('testname','test@ing.com', 'testpass')
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps({
                    'username': 'testname',
                    'email': 'test@ing.com',
                    'password': 'testpass',
                }),
                content_type='application/json',
                
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists', data['message'])
            self.assertIn('fail', data['status'])


user_correct = {
    'username': 'testname',
    'email': 'test@ing.com',
    'password': 'testpass',
}

user_no_email = {
    'username': 'testname',
    'password': 'testpass',
}

user_no_username = {
    'email': 'test@ing.com',
    'password': 'testpass',
}

user_no_pass = {
    'username': 'testname',
    'email': 'test@ing.com',
}

if __name__ == '__main__':
    unittest.main()