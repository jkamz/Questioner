"""
questions models
"""

from datetime import datetime

from psycopg2.extras import RealDictCursor
from app.database_connect import connect
from ..utils.errors import meetupexisterror, questionerror


class Questions():
    """
   define all questions attributes and methods
    """

    def __init__(self, meetup_id, title, body, author):
        """
        initialize Questions class
        """
        self.db = connect()
        self.meetup_id = meetup_id
        self.title = title
        self.body = body
        self.author = author
        self.created_on = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.votes = 0

    def check_meetup_exist(self):
        ''' Check if meetup is existent before posting question'''

        meetup_id = self.meetup_id
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query = """ SELECT meetup_id FROM meetups WHERE meetup_id = '%s'""" % (meetup_id)

        cur.execute(query)
        meetup = cur.fetchone()
        if meetup:
            return True

        return False

    def check_question_exist(self):
        """check if question is already in db"""
        title = self.title
        body = self.body
        author = self.author

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ SELECT question_id FROM questions WHERE title='{}' AND body='{}' AND author='{}' """.format(title, body, author)

        cur.execute(query)
        question = cur.fetchone()
        if question:
            return True

        return False

    def get_question_by_id(self, question_id):
        """check if a question exists using question id"""
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query = """ SELECT * FROM questions WHERE question_id = '%s'""" % (question_id)
        cur.execute(query)
        question = cur.fetchone()

        if question:
            return True

        return False

    def createQuestion(self):
        '''
        Method for creating a new question record
        '''

        # first ensure meetup exists
        if not self.check_meetup_exist():
            return meetupexisterror

        # check if comment is duplicate
        if self.check_question_exist():
            return questionerror

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """INSERT INTO questions (meetup_id, created_on,
        title, body, author, votes) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * """

        cur.execute(query, (self.meetup_id, self.created_on, self.title, self.body,
                            self.author, self.votes))

        question = cur.fetchone()
        self.db.commit()
        cur.close()

        return question

    def upvoteQuestion(self, question_id, username):
        '''
        Method for upvoting a question
        '''
        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ INSERT INTO votes (question_id, username) VALUES (%s, %s) """

        query1 = """ UPDATE questions SET votes = votes+1 WHERE id = {} RETURNING * """.format(
            question_id)

        cur.execute(query1)
        question = cur.fetchone()

        cur.execute(query, (question_id, username))
        self.db.commit()
        cur.close()

        return question, {"message": "upvote successful"}

    def downvoteQuestion(self, question_id, username):
        '''
        Method for upvoting a question
        '''
        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ INSERT INTO votes (question_id, username) VALUES (%s, %s) """

        query1 = """ UPDATE questions SET votes = votes-1 WHERE id = {} RETURNING * """.format(
            question_id)

        cur.execute(query1)
        question = cur.fetchone()

        cur.execute(query, (question_id, username))
        self.db.commit()
        cur.close()

        return question, {"message": "downvote successful"}
