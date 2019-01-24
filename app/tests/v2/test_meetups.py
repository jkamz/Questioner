"""
Tests for meetups operations
"""

import unittest
import json
from ... import create_app
from app.database_connect import destroy_database, create_tables, connect


class MeetupTest(unittest.TestCase):
    """class representing the meetups test case"""

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

        self.meetup = {
            "host": "jkamz",
            "location": "Nairobi",
            "happeningOn": "2020-01-16 19:00",
            "summary": "Getting to know python",
            "topic": "python"
        }

        self.meetup2 = {
            "host": "jkamz",
            "location": "Nairobi",
            "happeningOn": "2021-01-16 19:00",
            "summary": "Getting to know python",
            "topic": "node"
        }

        self.meetup1 = {}

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

    def test_create_meetup(self):
        '''test the endpoint of creating new meetup'''

        # create user and generate token
        self.register_and_login_user()

        res = self.client.post("api/v2/meetups", data=json.dumps(self.meetup), headers=self.headers)
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_data["data"])

    def test_create_invalid_meetup(self):
        '''test the endpoint of creating a new meetup record invalidly'''

        # create user and generate token
        self.register_and_login_user()

        res = self.client.post("api/v2/meetups", data=json.dumps(self.meetup1), headers=self.headers)

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertIn("expects only Application/JSON data", str(response_data))

    def test_get_one_meetup(self):
        '''test the endpoint for getting one meetup'''

        # create user and generate token
        self.register_and_login_user()

        # post/ create a meetup
        res = self.client.post("api/v2/meetups", data=json.dumps(self.meetup2), headers=self.headers)
        self.assertEqual(res.status_code, 200)

        # get one meetup by id
        get_res = self.client.get("api/v2/meetups/1")
        get_res_data = json.loads(get_res.data.decode())
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res_data["meetup"]["host"], "jkamz")

    def test_non_existent_meetup(self):
        '''test when the given meetup id is non existent'''
        get_res = self.client.get("api/v2/meetups/353")
        get_res_data = json.loads(get_res.data.decode())
        self.assertEqual(get_res.status_code, 404)
        self.assertEqual(get_res_data["message"], "meetup not found")

    def tearDown(self):
        ''' Purge all posted data before running tests again '''
        destroy_database()
