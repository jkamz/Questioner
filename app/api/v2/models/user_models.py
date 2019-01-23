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

    def __init__(self, email, username, password, firstname, lastname, phoneNumber, isAdmin):
        '''
        Initialize class
        '''

        self.db = connect()
        self.email = email
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phoneNumber = phoneNumber
        self.isAdmin = isAdmin

    def check_email_exist(self):
        """
        check if email is already registered
        """
        email = self.email
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query2 = """ SELECT email FROM users WHERE email = '%s'""" % (email)

        cur.execute(query2)
        user = cur.fetchone()
        if user:
            return True

        return False

    def check_username_exist(self):
        """
        check if username is already registered
        """
        username = self.username
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        query1 = """ SELECT username FROM users WHERE username = '%s'""" % (username)

        cur.execute(query1)
        user = cur.fetchone()
        if user:
            return True
        return False

    def signUp(self):
        '''
        Method for user sign up
        '''

        registered_on = datetime.now().strftime("%Y-%m-%d %H:%M")

        cur = self.db.cursor(cursor_factory=RealDictCursor)

        # first check if username is available
        if self.check_username_exist():
            return usernameerror

        # check if email is taken
        if self.check_email_exist():
            return emailerror

        # create user
        query = """ INSERT INTO users (firstname, lastname, email,
        phoneNumber, username, registered_on, password, isAdmin) VALUES (
        %s,%s,%s,%s,%s,%s,%s,%s) RETURNING * """

        cur.execute(query, (self.firstname, self.lastname, self.email,
                            self.phoneNumber, self.username, registered_on, self.password, self.isAdmin))
        user = cur.fetchone()
        self.db.commit()
        cur.close()

        dont_return = {"password", "registered_on"}

        def without_pass(d, keys):
            return {x: d[x] for x in d if x not in keys}

        return_user = without_pass(user, dont_return)

        return return_user, {"message": "User created successfully"}
