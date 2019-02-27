"""
questions models
"""

from datetime import datetime

from psycopg2.extras import RealDictCursor
from app.database_connect import connect
from ..utils.errors import meetupexisterror, questionerror, questionexisterror


class Questions():
    """
   define all questions attributes and methods
    """

    def __init__(self, meetup_id=None, title=None, body=None, author=None):
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
        body = self.body
        author = self.author

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ SELECT question_id FROM questions WHERE meetup_id='{}' AND body='{}' AND author='{}' """.format(self.meetup_id, body, author)

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

    def getQuestions(self):
        '''
        Method for getting questions for a specific meetup
        '''

        # first ensure meetup exists
        if not self.check_meetup_exist():
            return meetupexisterror

        meetup_id = self.meetup_id
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query = """ SELECT * FROM questions WHERE meetup_id = '%s'""" % (meetup_id)
        cur.execute(query)
        questions = cur.fetchall()

        return questions

    def getQuestion(self, question_id):
        '''
        Method for getting one question
        '''

        if not self.get_question_by_id(question_id):
            return questionexisterror

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ SELECT * FROM questions WHERE question_id='{}' """.format(question_id)

        cur.execute(query)
        question = cur.fetchone()

        return question

    def upvoteQuestion(self, question_id, username):
        '''
        Method for upvoting a question
        '''

        # first check if question exists
        if not self.get_question_by_id(question_id):
            return questionexisterror

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        # delete vote from downvotes table if exist
        query_delete_vote = """DELETE FROM downvotes WHERE username = '{}'
        and question_id = '{}';""".format(username, question_id)

        cur.execute(query_delete_vote)

        # check if upvote exists
        query_check_vote = """ SELECT * FROM upvotes WHERE question_id = '%s'
        AND username = '%s' """ % (question_id, username)

        cur.execute(query_check_vote)
        vote = cur.fetchone()
        if vote:
            return {"status": 400, "message": "Already voted"}

        # add upvote to question table
        query_upvote = """ UPDATE questions SET votes = votes+1 WHERE
        question_id = {} RETURNING * """.format(
            question_id)

        cur.execute(query_upvote)
        question = cur.fetchone()

        # add vote to upvotes table
        query = """ INSERT INTO upvotes (question_id, username) VALUES (%s, %s) """

        cur.execute(query, (question_id, username))
        self.db.commit()
        cur.close()

        return question, {"message": "upvote successful"}

    def downvoteQuestion(self, question_id, username):
        '''
        Method for upvoting a question
        '''

        # first check if question exists
        if not self.get_question_by_id(question_id):
            return questionexisterror

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        # delete vote from upvotes table if exist
        query_delete_vote = """DELETE FROM upvotes WHERE username = '{}'
        and question_id = '{}';""".format(username, question_id)

        cur.execute(query_delete_vote)

        # check if downvote exists
        query_check_vote = """ SELECT * FROM downvotes WHERE question_id = '%s'
        AND username = '%s' """ % (question_id, username)

        cur.execute(query_check_vote)
        vote = cur.fetchone()
        if vote:
            return {"status": 400, "message": "Already voted"}

        # add downvote to question table
        query_downvote = """ UPDATE questions SET votes = votes-1 WHERE
        question_id = {} RETURNING * """.format(
            question_id)

        cur.execute(query_downvote)
        question = cur.fetchone()

        # add vote to upvotes table
        query = """ INSERT INTO downvotes (question_id, username) VALUES (%s, %s) """

        cur.execute(query, (question_id, username))
        self.db.commit()
        cur.close()

        return question, {"message": "upvote successful"}
