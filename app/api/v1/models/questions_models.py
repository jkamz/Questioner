"""
questions models
"""

from datetime import datetime

questions = []


class Questions():
    """
   define all questions attributes and methods
    """

    def __init__(self, meetup_id):
        """
        initialize Questions class
        """
        self.meetup_id = meetup_id
        self.created_on = datetime.now()

    def createQuestion(self, meetup_id, title, body, author):
        '''
        Method for creating a new question record
        '''
        question = {
            "question_id": len(questions) + 1,
            "meetup_id": meetup_id,
            "title": title,
            "body": body,
            "author": author,
            "created_on": self.created_on,
            "votes": 0
        }

        questions.append(question)
        return question
