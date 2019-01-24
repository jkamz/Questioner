"""
Tests for questions operations
"""

import unittest
import json

from app.database_connect import destroy_database, create_tables, connect

from ... import create_app


class QuestionTest(unittest.TestCase):
    """class representing the questions test case"""

    def setUp(self):
        '''initialize the app and define test variable'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()

        connect()
        create_tables()

        self.user = {
            "firstname": "andela",
            "lastname": "bootcamp",
            "email": "andeelapac@pac.com",
            "phoneNumber": "+254705107566",
            "username": "andech",
            "password": "Jkamz6432@"
        }

        self.userlogin = {
            "username": "andech",
            "password": "Jkamz6432@"
        }

        self.question = {
            "author": "jkmz",
            "body": "what did you say?",
            "title": "what"
        }

        self.meetup = {
            "host": "jkamz",
            "location": "Nairobi",
            "happeningOn": "2020-01-16 19:00",
            "summary": "Getting to know python",
            "topic": "python"
        }

        self.question1 = {}

        self.vote = {
            "questionId": 1
        }

    def register_and_login_user(self):
        """Register and sign in user to get auth token"""
        # signup
        res = self.client.post("api/v2/auth/signup", data=json.dumps(self.user),
                               content_type="application/json")

        # sign in
        res1 = self.client.post("api/v2/auth/signin", data=json.dumps(self.userlogin),
                                content_type="application/json")

        response_data = json.loads(res1.data.decode())
        token = response_data["access_token"]

        self.headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json'
        }

        return self.headers

    def test_create_question(self):
        '''test the endpoint of creating new question record'''

        # create_user and generate token
        self.register_and_login_user()

        # post meetup
        res = self.client.post("api/v2/meetups", data=json.dumps(self.meetup), headers=self.headers)

        # post question
        res = self.client.post("api/v2/meetups/1/questions", data=json.dumps(self.question),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_data["data"])
        # self.assertIn("User created successfully", str(response_data))

    def test_create_invalid_question(self):
        '''test the endpoint of creating a new question record invalidly'''

        # create_user and generate token
        self.register_and_login_user()

        res = self.client.post("api/v2/meetups/1/questions", data=json.dumps(self.question1),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertIn("expects only Application/JSON data", str(response_data))

    def tearDown(self):
        ''' Purge all posted data before running tests again '''
        destroy_database()
