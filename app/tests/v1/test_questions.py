"""
Tests for meetups operations
"""

import unittest
import json
from ... import create_app


class QuestionTest(unittest.TestCase):
    """class representing the meetups test case"""

    def setUp(self):
        '''initialize the app and define test variable'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.app_context = self.app

        self.question = {
            "author": "jkamz",
            "body": "what did you say?",
            "created_on": "07:38am Saturday 12 January 2019",
            "meetup_id": 2,
            "question_id": 3,
            "title": "what",
            "votes": 0
        }

        self.question1 = {}

    def test_create_question(self):
        '''test the endpoint of creating new question record'''

        res = self.client.post("api/v1/questions", data=json.dumps(self.question),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_data["data"])

    def test_create_invalid_question(self):
        '''test the endpoint of creating a new question record invalidly'''

        res = self.client.post("api/v1/questions", data=json.dumps(self.question),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertFalse(response_data["data"])

    def test_upvote_question(self):
