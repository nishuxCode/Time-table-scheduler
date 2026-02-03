from flask import session
from front.user_dao import UserDao

class User:
    def __init__(self, username=None, password=None, email=None, country=None):
        self.username = username
        self.password = password
        self.email = email
        self.country = country

    def login_check(self):
        if session.get("login") == "true":
            return "success"
        return "error"

    def login(self):
        if UserDao.validate(self.username, self.password):
            session["login"] = "true"
            # Store user details in session (avoid storing the whole object if not needed)
            session["user"] = {
                "username": self.username,
                "email": self.email,
                "country": self.country
            }
            return "success"
        else:
            return "error"

    def register(self):
        if UserDao.register(self.username, self.password, self.email, self.country):
            return "success"
        return "error"

    def logout(self):
        session.clear()
        return "success"
