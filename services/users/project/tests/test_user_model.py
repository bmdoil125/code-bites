import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('testname','test@email.com')
        self.assertTrue(user.id)
        self.assertEqual(user.username,'testname')
        self.assertEqual(user.email,'test@email.com')
        self.assertTrue(user.active)

    def test_add_duplicate_username(self):
        user = add_user('testname','test@email.com')
        dup_user = User(username='testname', email='test2@email.com')
        db.session.add(dup_user)
        with self.assertRaises(IntegrityError): # Adding dup user should trigger integrity error
            db.session.commit()

    def test_add_duplicate_email(self):
        user = add_user('testname','test@email.com')
        dup_user = User(username='testname2', email='test@email.com')
        db.session.add(dup_user)
        with self.assertRaises(IntegrityError): # Adding dup user should trigger integrity error
            db.session.commit()

    def test_to_json(self):
        user = add_user('testname','test@email.com')
        self.assertTrue(isinstance(user.to_json(), dict)) # to_json method should result in a dict

if __name__ == '__main__':
    unittest.main()