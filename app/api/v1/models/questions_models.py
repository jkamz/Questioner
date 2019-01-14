"""
questions models
"""

from datetime import datetime

questions = []


class Questions():
    """
   define all questions attributes and methods
    """

    def __init__(self, meetup_id=None):
        """
        initialize Questions class
        """
        self.meetup_id = meetup_id
        self.created_on = datetime.now().strftime("%H:%M%P %A %d %B %Y")

    def createQuestion(self, title, body, author):
        '''
        Method for creating a new question record
        '''
        question = {
            "question_id": len(questions) + 1,
            "meetup_id": self.meetup_id,
            "title": title,
            "body": body,
            "author": author,
            "created_on": self.created_on,
            "votes": 0
        }

        questions.append(question)
        return question

    @staticmethod
    def upvoteQuestion(questionId):
        '''
        Method for upvoting a question
        '''
        question = [question for question in questions if question["question_id"] == questionId]

        if question:
            question[0]["votes"] += 1

            return question, {"message": "upvote successfull"}

        return None

    @staticmethod
    def downvoteQuestion(questionId):
        '''
        Method for upvoting a question
        '''
        question = [question for question in questions if question["question_id"] == questionId]

        if question:
            question[0]["votes"] -= 1

            return question, {"message": "downvote successfull"}

        return None