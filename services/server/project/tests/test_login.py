import json
import unittest
import sys
from project import db
from project.tests.base import BaseTestCase
from project.api.models import User
from project.tests.utils import add_user
from project import db
from project.api.models import User
from flask import current_app



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


    def test_user_reg_wrong_content_type(self):
        
        with self.client:
            response = self.client.post(
                '/login/register',
                data=json.dumps(user_reg_correct),
                content_type = 'text/html'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 406)
            self.assertIn('This endpoint only accepts json', data['message'])
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
                '/login/login',
                data=json.dumps(user_login),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Logged In')
            self.assertTrue(data['token'])
            self.assertTrue(response.content_type == 'application/json')
            

    def test_user_not_reg_login(self):
        """ Test unregistered user login """
        with self.client:
            response = self.client.post(
                '/login/login',
                data=json.dumps(user_login),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Username or password incorrect')
            self.assertTrue(response.content_type == 'application/json')

    def test_user_signout(self):
        add_user('testname', 'test@ing.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps(user_login),
                content_type='application/json'
            )
            login_data = json.loads(login_response.data.decode())
            token = login_data['token']

            response = self.client.get(
                '/login/signout',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Logged Out')
            self.assertEqual(response.status_code, 200)

    def test_user_signout_expired_token(self):
        """ Test signout with expired JWT """
        add_user('testname', 'test@ing.com', 'testpass')

        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1

        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps(user_login),
                content_type='application/json'
            )

            # get token from login response
            login_data = json.loads(login_response.data.decode())
            token = login_data['token']

            response = self.client.get(
                '/login/signout',
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Please log in again.')
            self.assertEqual(response.status_code, 403)

    def test_user_signout_invalid_token(self):
        """ Test signout with invalid JWT """
        token = 'garbage'
        with self.client:
            response = self.client.get(
                '/login/signout',
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Unauthorized')
            self.assertEqual(response.status_code, 403)

    def test_user_me(self):
        """ Test logged in user route """
        add_user('testname', 'test@ing.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps(user_login),
                content_type='application/json'
            )
            login_data = json.loads(login_response.data.decode())
            token = login_data['token']
            
            response = self.client.get(
                '/login/me',
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertTrue(data['message'] == 'Success')
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'testname')
            self.assertTrue(data['data']['email'] == 'test@ing.com')
            self.assertFalse(data['data']['admin'])
            self.assertEqual(response.status_code, 200)

    def test_user_me_invalid(self):
        """ Test logged in user route with invalid token """
        with self.client:
            response = self.client.get(
                '/login/me',
                headers={'Authorization': f'Bearer fail'},
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Unauthorized')
            self.assertEqual(response.status_code, 403)

    def test_user_signout_inactive(self):
        add_user('testname', 'test@ing.com', 'testpass')
        # update user to inactive
        user = User.query.filter_by(email='test@ing.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@ing.com',
                    'password': 'testpass'
                }),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            response = self.client.get(
                '/login/signout',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Unauthorized')
            self.assertEqual(response.status_code, 401)
            
    def test_user_me_inactive(self):
        """ Test GET /login/me endpoint inactive user """
        add_user('testname', 'test@ing.com', 'testpass')
        # update user to inactive
        user = User.query.filter_by(email='test@ing.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({
                    'email': 'test@ing.com',
                    'password': 'testpass'
                }),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            response = self.client.get(
                '/login/me',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Unauthorized')
            self.assertEqual(response.status_code, 401)



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