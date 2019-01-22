"""
Models for users attributes and methods
"""

from datetime import datetime
from psycopg2.extras import RealDictCursor
from app.database_connect import connect


class User():
    """
    define all User attributes and methods
    """

    def __init__(self):
        '''
        Initialize class
        '''

        self.db = connect()

    def signUp(self, firstname, lastname, email, phoneNumber, username, password, isAdmin):
        '''
        Method for user sign up
        '''

        registered_on = datetime.now().strftime("%Y-%m-%d %H:%M")

        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query = """ INSERT INTO users (firstname, lastname, email,
        phoneNumber, username, registered_on, password, isAdmin) VALUES (
        %S,%S,%S,%S,%S,%S,%S,%S) RETURNING * """

        cur.execute(query, (firstname, lastname, email,
                            phoneNumber, username, registered_on, password, isAdmin))
        user = cur.fetchone()
        self.db.commit()
        cur.close()

        dont_return = {"password", "registered"}

        def without_pass(d, keys):
            return {x: d[x] for x in d if x not in keys}

        return_user = without_pass(user, dont_return)

        return return_user, {"message": "User created successfully"}
