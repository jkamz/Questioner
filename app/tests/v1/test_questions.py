"""
Tests for questions operations
"""

import unittest
import json
from ... import create_app


class QuestionTest(unittest.TestCase):
    """class representing the questions test case"""

    def setUp(self):
        '''initialize the app and define test variable'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.app_context = self.app

        self.question = {
            "author": "jkamz",
            "body": "what did you say?",
            "meetup_id": 1,
            "title": "what"
        }

        self.meetup = {
            "host": "jkamz",
            "location": "Nairobi",
            "happeningOn": "28th Jan",
            "summary": "Getting to know python",
            "tags": "python pythonista flask",
            "topic": "python"
        }

        self.question1 = {}

        self.vote = {
            "questionId": 1
        }

    def test_create_question(self):
        '''test the endpoint of creating new question record'''

        # post meetup
        res = self.client.post("api/v1/create_meetup", data=json.dumps(self.meetup),
                               content_type="application/json")

        # post question
        res = self.client.post("api/v1/meetups/1/questions", data=json.dumps(self.question),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_data["data"])

    def test_create_invalid_question(self):
        '''test the endpoint of creating a new question record invalidly'''

        res = self.client.post("api/v1/meetups/1/questions", data=json.dumps(self.question1),
                               content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertIn("expects only Application/JSON data", str(response_data))

    def test_upvote_question(self):
        '''test the endpoint of upvoting a question'''

        # upvote question
        res = self.client.patch("api/v1/questions/1/upvote", data=json.dumps(self.vote),
                                content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertIn("upvote successfull", str(response_data))

    def test_invalid_upvote_question(self):
        '''test the endpoint of upvoting an inexistent question'''

        # upvote question
        res = self.client.patch("api/v1/questions/456/upvote", data=json.dumps(self.vote),
                                content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertIn("upvote not successful", str(response_data))

    def test_downvote_question(self):
        '''test the endpoint of downvoting a question'''

        # downvote question
        res = self.client.patch("api/v1/questions/1/downvote", data=json.dumps(self.vote),
                                content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertIn("downvote successfull", str(response_data))

    def test_invalid_downvote_question(self):
        '''test the endpoint of downvoting an inexistent question'''

        # downvote question
        res = self.client.patch("api/v1/questions/456/downvote", data=json.dumps(self.vote),
                                content_type="application/json")

        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertIn("downvote not successful", str(response_data))
