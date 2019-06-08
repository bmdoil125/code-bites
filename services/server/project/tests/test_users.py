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
        response = self.client.get(
            '/users/ping',
            content_type='application/json'
            )
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
            response = self.client.get(
                f'/users/{user.id}',
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('testuser', data['data']['username'])
            self.assertIn('success', data['status'])

    def test_get_user_no_id(self):
        """ Error if id not provided """
        with self.client:
            response = self.client.get(
                '/users/fail',
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_user_incorrect_id(self):
        """ Error if incorrect id provided """
        with self.client:
            response = self.client.get(
                '/users/1337',
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])
                
    def test_get_all_users(self):
        """ Ensure get all users behaves correctly """
        # Add test users
        add_user('testuser1', 'testing123@gmail.com', 'testpass')
        add_user('testuser2', 'testingagain@gmail.com', 'testpass')
        add_admin_user('admin', 'admin@admin.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({'email': 'admin@admin.com', 'password': 'testpass'}),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            response = self.client.get(
                '/users',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 3)
            self.assertIn('success', data['status'])
            self.assertIn('testuser1', data['data']['users'][0]['username'])
            self.assertIn('testing123@gmail.com', data['data']['users'][0]['email'])
            self.assertTrue(data['data']['users'][0]['active'])
            self.assertFalse(data['data']['users'][0]['admin'])
            self.assertIn('testuser2', data['data']['users'][1]['username'])
            self.assertIn('testingagain@gmail.com', data['data']['users'][1]['email'])
            self.assertTrue(data['data']['users'][1]['active'])
            self.assertFalse(data['data']['users'][1]['admin'])

    
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
            self.assertTrue(data['message'] == 'Forbidden')
            self.assertEqual(response.status_code, 403)

    def test_update_user_admin(self):
        user = add_user('testname', 'test@ing.com', 'testpass')
        # add admin user and log in
        add_admin_user('admin', 'admin@admin.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({'email': 'admin@admin.com', 'password': 'testpass'}),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            get_response = self.client.get(
                f'/users/{user.id}',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
                )
            data = json.loads(get_response.data.decode())
            print(data)
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('testname', data['data']['username'])
            self.assertIn('test@ing.com', data['data']['email'])

            put_response = self.client.put(
                f'/users/{user.id}',
                data=json.dumps({'username': 'brent'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            put_data = json.loads(put_response.data.decode())
            print(put_data)
            self.assertEqual(put_response.status_code, 201)
            self.assertIn('brent', put_data['data']['username'])
            self.assertIn('success', put_data['status'])

    
    def test_update_user_self(self):
        user = add_user('testname', 'test@ing.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({'email': 'test@ing.com', 'password': 'testpass'}),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            get_response = self.client.get(
                f'/users/{user.id}',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
                )
            data = json.loads(get_response.data.decode())
            print(data)
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('testname', data['data']['username'])
            self.assertIn('test@ing.com', data['data']['email'])

            put_response = self.client.put(
                f'/users/{user.id}',
                data=json.dumps({'username': 'brent'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            put_data = json.loads(put_response.data.decode())
            print(put_data)
            self.assertEqual(put_response.status_code, 201)
            self.assertIn('brent', put_data['data']['username'])
            self.assertIn('success', put_data['status'])

    def test_update_user_unauthorized(self):
        add_user('testname', 'test@ing.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({'email': 'test@ing.com', 'password': 'testpass'}),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            user_to_update = add_user('updateme', 'up@date.com', 'testpass')
            get_response = self.client.get(
                f'/users/{user_to_update.id}',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
                )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('updateme', data['data']['username'])
            self.assertIn('up@date.com', data['data']['email'])

            put_response = self.client.put(
                f'/users/{user_to_update.id}',
                data=json.dumps({'username': 'brent'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            put_data = json.loads(put_response.data.decode())
            self.assertEqual(put_response.status_code, 403)
            self.assertIn('fail', put_data['status'])
            self.assertIn('You do not have permission to update this user', put_data['message'])

    def test_delete_user_admin(self):
        user = add_user('testname', 'test@ing.com', 'testpass')
        # add admin user and log in
        add_admin_user('admin', 'admin@admin.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({'email': 'admin@admin.com', 'password': 'testpass'}),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            get_response = self.client.get(
                f'/users/{user.id}',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
                )
            data = json.loads(get_response.data.decode())
            print(data)
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('testname', data['data']['username'])
            self.assertIn('test@ing.com', data['data']['email'])

            delete_response = self.client.delete(
                f'/users/{user.id}',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            self.assertEqual(delete_response.status_code, 204)

    def test_delete_user_self(self):
        user = add_user('testname', 'test@ing.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({'email': 'test@ing.com', 'password': 'testpass'}),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            get_response = self.client.get(
                f'/users/{user.id}',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
                )
            data = json.loads(get_response.data.decode())
            print(data)
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('testname', data['data']['username'])
            self.assertIn('test@ing.com', data['data']['email'])

            delete_response = self.client.delete(
                f'/users/{user.id}',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            self.assertEqual(delete_response.status_code, 204)
            

    def test_delete_user_unauthorized(self):
        add_user('testname', 'test@ing.com', 'testpass')
        with self.client:
            login_response = self.client.post(
                '/login/login',
                data=json.dumps({'email': 'test@ing.com', 'password': 'testpass'}),
                content_type='application/json'
            )
            token = json.loads(login_response.data.decode())['token']
            user_to_delete = add_user('deleteme', 'del@ete.com', 'testpass')
            get_response = self.client.get(
                f'/users/{user_to_delete.id}',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
                )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertIn('deleteme', data['data']['username'])
            self.assertIn('del@ete.com', data['data']['email'])

            delete_response = self.client.delete(
                f'/users/{user_to_delete.id}',
                content_type='application/json'
            )
            delete_data = json.loads(delete_response.data.decode())
            print(delete_data)
            self.assertEqual(delete_response.status_code, 403)
            self.assertIn('fail', delete_data['status'])
            self.assertIn('Forbidden', delete_data['message'])


    def test_delete_all_users(self):
        """ Ensure DELETE /users returns 405 """
        with self.client:
            response = self.client.delete('/users')
            self.assertEqual(response.status_code, 405)

    def test_update_all_users(self):
        """ Ensure PUT /users returns 405 """
        with self.client:
            response = self.client.put('/users')
            self.assertEqual(response.status_code, 405)





if __name__ == '__main__':
    unittest.main()