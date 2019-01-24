"""
questions models
"""

from datetime import datetime

from psycopg2.extras import RealDictCursor
from app.database_connect import connect
from ..utils.errors import meetupexisterror


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
        self.created_on = datetime.now().strftime("%H:%M%P %A %d %B %Y")
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

    def createQuestion(self):
        '''
        Method for creating a new question record
        '''

        # first ensure meetup exists
        if not self.check_meetup_exist():
            return meetupexisterror

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """INSERT INTO questions (meetup_id, created_on,
        title, body, author, votes) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * """

        cur.execute(query, (self.meetup_id, self.created_on, self.title, self.body,
                            self.author, self.votes))

        question = cur.fetchone()
        self.db.commit()
        cur.close()

        return question
