"""
Tests for questions operations
"""

import unittest
import json
from ... import create_app


class UserTest(unittest.TestCase):
    """class representing the users test case"""

    def setUp(self):
        '''initialize the app and define test variable'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.app_context = self.app

        self.user = {
            "firstname": "andela",
            "lastname": "bootcamp",
            "email": "andela.pac@pac.com",
            "username": "andech",
            "isAdmin": True,
            "password": "jkamz"
        }

        self.user1 = {
        }

        self.userlogin = {
            "username": "andech",
            "password": "jkamz",
            "isAdmin": True
        }

    def test_user_sign_up(self):
        '''test the endpoint for signing up a new user'''
        res = self.client.post("api/v1/signup", data=json.dumps(self.user),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_data["data"])
        self.assertIn("User created successfully", str(response_data))

    def test_invalid_user_sign_up(self):
        '''test the endpoint for signing up a new user invalidly'''
        res = self.client.post("api/v1/signup", data=json.dumps(self.user1),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertIn("expects only Application/JSON data", str(response_data))

    def test_user_sign_in(self):
        '''test endpoint for user sign in'''
        # first signup user
        res = self.client.post("api/v1/signup", data=json.dumps(self.user),
                               content_type="application/json")

        # sign in
        res = self.client.post("api/v1/signin", data=json.dumps(self.userlogin),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_data["data"])
        self.assertIn("Admin andech successfully signed in", str(response_data))

    def test_invalid_user_sign_in(self):
        '''test the endpoint for signing in invalidly/ without inputing data'''
        res = self.client.post("api/v1/signin", data=json.dumps(self.user1),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertIn("expects only Application/JSON data", str(response_data))
