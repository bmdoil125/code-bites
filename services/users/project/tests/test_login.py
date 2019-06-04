import json
import unittest

from project import db
from project.tests.base import BaseTestCase
from project.api.models import User
from project.tests.utils import add_user



class TestLoginRoute(BaseTestCase):
    """ Test user registration flow """
    def test_user_reg(self):
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_reg_correct),
                content_type = 'application/json'
            )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Registered')
        self.assertTrue(response.content_type == 'application/json')
        self.assertTrue(response.status_code, 201)
        self.assertTrue(data['token'])
    
    def test_user_reg_empty_payload(self):
        """ Test user registering with empty payload """
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
        """ Test user sending wrong content type """
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_reg_correct),
                content_type = 'text/html'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid header: Content-Type', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_reg_invalid_username(self):
        """ Test user registration with no username """
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_reg_no_username),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])


    def test_user_reg_invalid_email(self):
        """ Test user registration with no email """
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_reg_no_email),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_reg_missing_password(self):
        """ Test user registering with missing password """
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_reg_no_pass),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_reg_duplicate_email(self):
        """ Test user registering with duplicate email """
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

    def test_user_reg_login(self):
        """ Test registered user login flow """
        with self.client:
            add_user('testname', 'test@ing.com', 'testpass')
            response = self.client.post(
                '/login',
                data=json.dumps(user_login),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            print(response.status_code)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Logged In')
            self.assertTrue(data['token'])
            self.assertTrue(response.content_type == 'application/json')
            

    def test_user_not_reg_login(self):
        """ Test unregistered user login """
        with self.client:
            response = self.client.post(
                '/login',
                data=json.dumps(user_login),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            print(response.status_code)
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Username or password incorrect')
            self.assertTrue(response.content_type == 'application/json')



user_reg_correct = {
    'username': 'testname',
    'email': 'test@ing.com',
    'password': 'testpass',
}

user_reg_no_email = {
    'username': 'testname',
    'password': 'testpass',
}

user_reg_no_username = {
    'email': 'test@ing.com',
    'password': 'testpass',
}

user_reg_no_pass = {
    'username': 'testname',
    'email': 'test@ing.com',
}

user_login = {
    'email': 'test@ing.com',
    'password': 'testpass'
}

if __name__ == '__main__':
    unittest.main()