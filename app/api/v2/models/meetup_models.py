"""
meetups models
"""

from datetime import datetime

from psycopg2.extras import RealDictCursor
from app.database_connect import connect
from ..utils.errors import meetuperror


class Meetup():
    """
    define all meetup attributes and methods
    """

    def __init__(self, happeningOn=None, host=None, topic=None, summary=None, location=None):
        '''
        initialize class
        '''
        self.db = connect()
        self.created_on = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.happeningOn = happeningOn
        self.host = host
        self.topic = topic
        self.summary = summary
        self.location = location

    def check_user_status(self, username):
        """check if user is admin"""
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query1 = """ SELECT isAdmin FROM users WHERE username = '%s'""" % (username)

        cur.execute(query1)
        user = cur.fetchone()
        return user

    def check_user_id(self, username):
        """fetch user id"""

        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query = """ SELECT * FROM users WHERE username = '%s'""" % (username)

        cur.execute(query)
        user = cur.fetchone()
        return user["user_id"]

    def check_meetup_exists(self):
        """check if meetup is already in db"""
        happeningOn = self.happeningOn
        topic = self.topic
        location = self.location

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ SELECT meetup_id FROM meetups WHERE happeningOn='{}'
        AND topic='{}' AND location='{}' """.format(happeningOn, topic, location)

        cur.execute(query)
        meetup = cur.fetchall()
        if meetup:
            return True

        return False

    def check_rsvp_exists(self, user_id, meetup_id, response):
        """check if reservation exists already"""
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query = """ SELECT * FROM rsvps WHERE user_id = '{}' AND meetup_id = '{}'
         AND response = '{}' ORDER BY user_id DESC LIMIT 1""".format(user_id, meetup_id, response)

        cur.execute(query)
        rsvp = cur.fetchone()
        if rsvp:
            return True

        return False

    def createMeetup(self):
        '''
        Method for creating a new meetup record
        '''

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        # first check if meetup exists
        if self.check_meetup_exists():
            return meetuperror

        query = """INSERT INTO meetups (created_on, happeningOn, host, topic,
        summary, location) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING * """

        cur.execute(query, (self.created_on, self.happeningOn, self.host, self.topic,
                            self.summary, self.location))

        meetup = cur.fetchone()
        self.db.commit()
        cur.close()

        return meetup

    def getMeetup(self, meetup_id):
        '''
        Method for getting one meetup record
        '''
        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = " SELECT * FROM meetups WHERE meetup_id = '{}'".format(meetup_id)

        cur.execute(query)
        meetup = cur.fetchone()
        return meetup

    def allMeetups(self):
        '''method for getting all meetup records'''

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ SELECT * FROM meetups """

        cur.execute(query)
        meetups = cur.fetchall()
        return meetups

    def allUpcomingMeetups(self):
        '''method for getting all upcoming meetup records'''
        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = """ SELECT * FROM meetups """

        cur.execute(query)
        meetups = cur.fetchall()
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        x = [meetup for meetup in meetups if meetup["happeningon"] > date]
        return x

    def meetupRsvp(self, meetup_id, user_id, response, current_user):
        '''
        Method for getting rsvp meetup
        '''
        cur = self.db.cursor(cursor_factory=RealDictCursor)

        query = "INSERT INTO rsvps (meetup_id, user_id, response) VALUES (%s, %s, %s) RETURNING *"

        cur.execute(query, (meetup_id, user_id, response))
        rsvp_data = cur.fetchone()
        self.db.commit()
        cur.close()

        return rsvp_data, {"message": f"attendance status confirmed for {current_user}"}
