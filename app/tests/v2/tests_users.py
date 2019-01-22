"""
Tests for questions operations
"""

import unittest
import json

from app.database_connect import connect, destroy_database, create_tables

from ... import create_app


class UserTest(unittest.TestCase):
    """class representing the users test case"""

    def setUp(self):
        '''initialize the app and define test variable'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.app_context = self.app

        create_tables()

        self.user = {
            "firstname": "andela",
            "lastname": "bootcamp",
            "email": "andelapac@pac.com",
            "username": "andech",
            "phoneNumber": "+254705107566",
            "password": "Jkamz6432@"
        }

        self.user2 = {
            "firstname": "andela",
            "lastname": "bootcamp",
            "email": "andelapac2@pac.com",
            "phoneNumber": "+254705107566",
            "username": "andech2",
            "password": "Jkamz6432@"
        }

        self.user1 = {
        }

    def test_user_sign_up(self):
        '''test the endpoint for signing up a new user'''
        res = self.client.post("api/v2/auth/signup", data=json.dumps(self.user),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_data["data"])
        self.assertIn("User created successfully", str(response_data))

    def tearDown(self):
        ''' Purge all posted data before running tests again '''
