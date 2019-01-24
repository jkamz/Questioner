"""
comments models
"""

from datetime import datetime

from psycopg2.extras import RealDictCursor
from app.database_connect import connect
from ..utils.errors import questionexisterror, commenterror


class Comment():
    """
    define all comment attributes and methods
    """

    def __init__(self, question_id, body, author):
        '''
        initialize class
        '''
        self.db = connect()
        self.created_on = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.body = body
        self.author = author
        self.question_id = question_id

    def check_question_exist(self):
        ''' Check if question is existent before posting comment'''

        question_id = self.question_id
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query = """ SELECT question_id FROM questions WHERE question_id = '%s'""" % (question_id)

        cur.execute(query)
        question = cur.fetchone()
        if question:
            return True

        return False

    def check_comment_exist(self):
        """check if comment is already in db"""
        body = self.body
        author = self.author

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ SELECT comment_id FROM comments WHERE body='{}' AND author='{}' """.format(body, author)

        cur.execute(query)
        comment = cur.fetchone()
        if comment:
            return True

        return False

    def createComment(self):
        '''
        Method for creating a new comment record
        '''

        # first ensure question exists
        if not self.check_question_exist():
            return questionexisterror

        # check if comment is duplicate
        if self.check_comment_exist():
            return commenterror

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """INSERT INTO comments (question_id, body,
        author) VALUES (%s, %s, %s) RETURNING * """

        cur.execute(query, (self.question_id, self.body, self.author))

        comment = cur.fetchone()
        self.db.commit()
        cur.close()

        return comment
