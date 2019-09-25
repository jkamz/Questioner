"""
Tests for users operations
"""

import unittest
import json

from app.database_connect import destroy_database, create_tables, connect

from ... import create_app


class TestUser(unittest.TestCase):
    """class representing the users test case"""

    def setUp(self):
        '''initialize the app and define test variable'''

        config_name = "testing"

        self.app = create_app(config_name)
        self.client = self.app.test_client()

        connect()
        create_tables()

        self.user = {
            "firstname": "andela",
            "lastname": "bootcamp",
            "email": "andeelapac@pac.com",
            "phoneNumber": "+254705107566",
            "username": "andech",
            "password": "ABCD1234@"
        }

        self.user2 = {
            "firstname": "andela",
            "lastname": "bootcamp",
            "email": "andelapac2@pac.com",
            "phoneNumber": "+254705107566",
            "username": "andech2",
            "password": "ABCD1234@"
        }

        self.user1 = {
        }
        self.userlogin = {
            "username": "andech",
            "password": "ABCD1234@"
        }

    def test_user_sign_up(self):
        '''test the endpoint for signing up a new user'''

        res = self.client.post("api/v2/auth/signup", data=json.dumps(self.user),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_data["data"])
        self.assertIn("User created successfully", str(response_data))

    def test_invalid_user_sign_up(self):
        '''test the endpoint for signing up a new user invalidly'''
        res = self.client.post("/api/v2/auth/signup", data=json.dumps(self.user1),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertIn("expects only Application/JSON data", str(response_data))

    def test_user_sign_in(self):
        '''test endpoint for user sign in'''
        # first signup user
        res = self.client.post("api/v2/auth/signup", data=json.dumps(self.user),
                               content_type="application/json")

        # sign in
        res = self.client.post("api/v2/auth/signin", data=json.dumps(self.userlogin),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_data["data"])
        self.assertIn("Successfully signed is as andech", str(response_data))

    def test_invalid_user_sign_in(self):
        '''test the endpoint for signing in invalidly/ without inputing data'''
        res = self.client.post("api/v2/auth/signin", data=json.dumps(self.user1),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertIn("expects only Application/JSON data", str(response_data))

    def tearDown(self):
        ''' Purge all posted data before running tests again '''
        destroy_database()
