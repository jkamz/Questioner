"""
Tests for meetups operations
"""

import unittest
import json
from ... import create_app


class MeetupTest(unittest.TestCase):
    """class representing the meetups test case"""

    def setUp(self):
        '''initialize the app and define test variable'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.app_context = self.app

        self.meetup = {
            "created_on": "Thu, 10 Jan 2019 18:17:59 GMT",
            "host": "jkamz",
            "location": "Nairobi",
            "meetupId": "1",
            "occuring_on": "28th Jan",
            "summary": "Getting to know python",
            "tags": "python pythonista flask",
            "topic": "python"
        }

        self.rsvp = {
            "userId": "1",
            "attendance": "yes"
        }

    def test_create_meetup(self):
        '''test the endpoint of creating new meetup'''

        res = self.client.post("api/v1/create_meetup", data=json.dumps(self.meetup), content_type="application/json")
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_data["data"])
        self.assertIn("Meetup created successfully", str(response_data))

    def test_get_one_meetup(self):
        '''test the endpoint for getting one meetup'''

        # first post/ create a meetup
        res = self.client.post("api/v1/create_meetup", data=json.dumps(self.meetup), content_type="application/json")
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)

        # get one meetup by id
        get_res = self.client.get("api/v1/meetups/1")
        get_res_data = json.loads(get_res.data.decode())
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res_data["meetup"][1]["message"], "success")

    def test_non_existent_meetup(self):
        '''test when the given meetup id is non existent'''
        get_res = self.client.get("api/v1/meetups/353")
        get_res_data = json.loads(get_res.data.decode())
        self.assertEqual(get_res.status_code, 404)
        self.assertEqual(get_res_data["message"], "meetup not found")

    def test_get_all_meetups(self):
        '''test the endpoint for getting all meetups'''
        res = self.client.get("api/v1/meetups")
        res_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["message"], "success")
