import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('testname','test@email.com', 'testpass')
        self.assertTrue(user.id)
        self.assertEqual(user.username,'testname')
        self.assertEqual(user.email,'test@email.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertFalse(user.admin)

    def test_add_duplicate_username(self):
        add_user('testname','test@email.com', 'testpass')
        dup_user = User(username='testname', email='test2@email.com', password='testpass')
        db.session.add(dup_user)
        with self.assertRaises(IntegrityError): # Adding dup user should trigger integrity error
            db.session.commit()

    def test_add_duplicate_email(self):
        add_user('testname','test@email.com', 'testpass')
        dup_user = User(username='testname2', email='test@email.com', password='testpass')
        db.session.add(dup_user)
        with self.assertRaises(IntegrityError): # Adding dup user should trigger integrity error
            db.session.commit()

    def test_to_json(self):
        user = add_user('testname','test@email.com', 'testpass')
        self.assertTrue(isinstance(user.to_json(), dict)) # to_json method should result in a dict

    def test_passwords(self):
        user_one = add_user('test', 'test@test.com', 'testpass')
        user_two = add_user('test2', 'test2@test.com', 'testpass')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_jwt(self):
        user = add_user('test', 'test@test.com', 'testpass')
        token = user.encode_jwt(user.id)
        self.assertTrue(isinstance(token, bytes))

    def test_decode_jwt(self):
        user = add_user('test','test@test.com', 'testpass')
        token = user.encode_jwt(user.id)
        self.assertTrue(isinstance(token, bytes))
        self.assertEqual(User.decode_jwt(token), user.id)

if __name__ == '__main__':
    unittest.main()