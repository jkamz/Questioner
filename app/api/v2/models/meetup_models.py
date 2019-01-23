"""
meetups models
"""

from datetime import datetime

from psycopg2.extras import RealDictCursor
from app.database_connect import connect


class Meetup():
    """
    define all meetup attributes and methods
    """

    def __init__(self, happeningOn=None, host=None, topic=None, summary=None, location=None):
        '''
        initialize class
        '''
        self.created_on = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.happeningOn = happeningOn
        self.host = host
        self.topic = topic
        self.summary = summary
        self.location = location

    def createMeetup(self):
        '''
        Method for creating a new meetup record
        '''
        db = connect()

        cur = db.cursor(cursor_factory=RealDictCursor)

        query = """INSERT INTO meetups (created_on, happeningOn, host, topic,
        summary, location) VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING * """

        cur.execute(query, (self.created_on, self.happeningOn, self.host, self.topic,
                            self.summary, self.location))

        meetup = cur.fetchone()
        db.commit()
        cur.close()

        return meetup

    def getMeetup(self, meetupId):
        '''
        Method for getting one meetup record
        '''
        pass

    def allMeetups(self):
        '''method for getting all meetup records'''
        pass

    def allUpcomingMeetups(self):
        '''method for getting all upcoming meetup records'''
        pass

    def meetupRsvp(self, userId, meetupId, response):
        '''
        Method for getting rsvp meetup
        '''
