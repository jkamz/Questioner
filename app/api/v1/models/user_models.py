"""
Models for users attributes and methods
"""

from datetime import datetime

users = []


class User():
    """
    define all User attributes and methods
    """

    def __init__(self):
        '''
        Initialize class
        '''

    def signUp(self, firstname, lastname, username, email, password, isAdmin):
        '''
        Method for user sign up
        '''
        user = {
            "id": len(users) + 1,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "username": username,
            "registered": datetime.now().strftime("%H:%M%P %A %d %B %Y"),
            "isAdmin": isAdmin,
            "password": password
        }

        users.append(user)
        return user, {"message": "User created successfully"}

    @staticmethod
    def signIn(username, password, isAdmin):
        '''
        Method for user sign up
        '''

        user = [user for user in users if user["username"] == username
                and user["password"] == password]

        if user:
            if user[0]["isAdmin"] == isAdmin:
                return f"Admin {username} successfully signed in"
            return f"{username} successfully signed in"

        return "Invalid Username or Password"
