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

    def test_create_meetup(self):
        '''test the endpoint of creating new meetup'''

        res = self.client.post("api/v2/meetups", data=json.dumps(self.meetup),
                               content_type="application/json")
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_data["data"])

    def test_create_invalid_meetup(self):
        '''test the endpoint of creating a new meetup record invalidly'''

        res = self.client.post("api/v2/meetups", data=json.dumps(self.meetup1),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertIn("expects only Application/JSON data", str(response_data))

    def tearDown(self):
        ''' Purge all posted data before running tests again '''
        destroy_database()
