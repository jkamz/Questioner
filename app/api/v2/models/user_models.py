"""
Models for users attributes and methods
"""
from datetime import datetime


from psycopg2.extras import RealDictCursor
from app.database_connect import connect
from ..utils.errors import usernameerror, emailerror


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

        # first check if username is available
        query1 = """ SELECT username FROM users WHERE username = '%s'""" % (username)

        cur.execute(query1)
        user = cur.fetchone()
        if user is not None:
            return usernameerror

        # check if email is taken
        query2 = """ SELECT email FROM users WHERE email = '%s'""" % (email)

        cur.execute(query2)
        user = cur.fetchone()
        if user is not None:
            return emailerror

        # create user
        query = """ INSERT INTO users (firstname, lastname, email,
        phoneNumber, username, registered_on, password, isAdmin) VALUES (
        %s,%s,%s,%s,%s,%s,%s,%s) RETURNING * """

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
