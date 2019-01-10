"""
meetups models
"""

from datetime import datetime

meetups = []


class Meetup():
    """
    define all meetup attributes and methods
    """

    def __init__(self, occuring_on, host, topic, summary, tags, location):
        '''
        initialize class
        '''
        self.meetupId = len(meetups) + 1
        self.created_on = datetime.now()
        self.occuring_on = occuring_on
        self.host = host
        self.topic = topic
        self.summary = summary
        self.tags = tags
        self.location = location

    def createMeetup(self):
        '''
        Method for creating a new meetup record
        '''

        meetup = {
            "id": self.meetupId,
            "host": self.host,
            "created_on": self.created_on,
            "occuring_on": self.occuring_on,
            "topic": self.topic,
            "summary": self.summary,
            "location": self.location,
            "tags": self.tags
        }

        meetups.append(meetup)
        return meetup, {"message": "Meetup created successfully"}
