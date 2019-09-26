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
        query = """ SELECT meetup_id FROM meetups WHERE meetup_id = '%s'""" % (
            meetup_id)

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

        query = """ SELECT question_id FROM questions WHERE meetup_id='{}' AND body='{}' AND author='{}' """.format(
            self.meetup_id, body, author)

        cur.execute(query)
        question = cur.fetchone()
        if question:
            return True

        return False

    def get_question_by_id(self, question_id):
        """check if a question exists using question id"""
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query = """ SELECT * FROM questions WHERE question_id = '%s'""" % (
            question_id)
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
        query = """ SELECT * FROM questions WHERE meetup_id = '%s'""" % (
            meetup_id)
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

        query = """ SELECT * FROM questions WHERE question_id='{}' """.format(
            question_id)

        cur.execute(query)
        question = cur.fetchone()

        return question

    def cursorOps(self, query):
        '''
        Method to open, execute, and close cursor
        '''

        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        self.db.commit()
        cur.close()

    def queries(self, question_id, username):
        queries = {
            'query_delete_downvote': """DELETE FROM downvotes WHERE username = '{}'
                and question_id = '{}';""".format(username, question_id),
            'query_upvote': """ UPDATE questions SET votes = votes+1 WHERE
                question_id = {} RETURNING * """.format(question_id),
            'query_check_downvote': """ SELECT * FROM downvotes WHERE question_id = '%s'
                AND username = '%s' """ % (question_id, username),
            'query_delete_upvote': """DELETE FROM upvotes WHERE username = '{}'
                and question_id = '{}';""".format(username, question_id),
            'query_downvote': """ UPDATE questions SET votes = votes-1 WHERE
                question_id = {} RETURNING * """.format(question_id),
            'query_check_vote': """ SELECT * FROM upvotes WHERE question_id = '%s'
                AND username = '%s' """ % (question_id, username)
        }

        return queries

    def upvoteQuestion(self, question_id, username):
        '''
        Method for upvoting a question
        '''
        if not self.get_question_by_id(question_id):
            return questionexisterror

        queries = self.queries(question_id, username)

        # If there is a downvote, remove it and add question votes by 1
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(queries['query_check_downvote'])
        downvote = cur.fetchone()
        self.db.commit()
        cur.close()

        if downvote:
            self.del_dwv_and_vote(queries)
            # self.cursorOps(queries['query_delete_downvote'])
            # self.cursorOps(queries['query_upvote'])
        else:
            pass

        # if there is an upvote, remove it and decrease votes by one
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(queries['query_check_vote'])
        vote = cur.fetchone()
        self.db.commit()
        cur.close()

        if vote:
            self.del_upv_and_dwv(queries)
            return vote, {"message": "removed upvote successfully"}

        # add upvote to question table
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(queries['query_upvote'])
        question = cur.fetchone()
        self.db.commit()
        cur.close()

        # add vote to upvotes table
        query = """ INSERT INTO upvotes (question_id, username) VALUES (%s, %s) """

        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (question_id, username))
        self.db.commit()
        cur.close()

        return question, {"message": "upvote successful"}

    def downvoteQuestion(self, question_id, username):

        if self.getQuestion(question_id) == questionexisterror:
            return questionexisterror

        queries = self.queries(question_id, username)

        # If there is an upvote, remove it and decrease question votes by 1
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(queries['query_check_vote'])
        upvote = cur.fetchone()
        self.db.commit()
        cur.close()

        if upvote:
            self.del_upv_and_dwv(queries)
        else:
            pass

        # if there is a downvote, remove it and increase votes by one
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(queries['query_check_downvote'])
        vote = cur.fetchone()
        self.db.commit()
        cur.close()

        if vote:
            self.del_dwv_and_vote(queries)
            return vote, {"message": "removed downvote successfully"}

        # add downvote to question table
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(queries['query_downvote'])
        question = cur.fetchone()
        self.db.commit()
        cur.close()

        # add vote to downvotes table
        query = """ INSERT INTO downvotes (question_id, username) VALUES (%s, %s) """

        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (question_id, username))
        self.db.commit()
        cur.close()

        return question, {"message": "downvote successful"}

    def del_dwv_and_vote(self, queries):
        self.cursorOps(queries['query_delete_downvote'])
        self.cursorOps(queries['query_upvote'])

    def del_upv_and_dwv(self, queries):
        self.cursorOps(queries['query_delete_upvote'])
        self.cursorOps(queries['query_downvote'])
