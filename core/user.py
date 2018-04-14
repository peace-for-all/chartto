import database


class User:
    def __init__(self, username):
        self.username = username
        self.db = database.Database()
        self.user_id = self.get_id()

    def get_token(self):
        """Returns token, if we store it somewhere"""
        token = self.db.query("SELECT api_token FROM Users WHERE username = '{}'".format(self.username))
        if token:
            self.token = token
            return token
        else:
            print "No token obtained"
            return False

    def get_id(self):
        """Creates id, if not found in db, or returns from db""" # FIXME - double check queryes for escaping!
        user_id = self.db.query("SELECT user_id FROM Users WHERE username = '{}'".format(self.username))
        if not user_id:
            user_id = self.create_id()
            save = self.db.query("INSERT INTO Users (user_id, username) VALUES (" + user_id + ", " + self.username + ")")
            if save:
                self.user_id = user_id
            else:
                raise ValueError('Could not create user_id for user and save')

        return user_id

    def create_id(self):
        """Creates id for user"""
        max_id = self.db.query("SELECT max(user_id) FROM Users")
        if max_id:
            return int(max_id) + 1
        return False

    def save_data(self):
        """Persists user data on disk"""
        query = "INSERT INTO Users (user_id, username, api_token) VALUES (" \
        + self.user_id + ", " + self.username + ", " + self.token + ")"
        if self.db.query(query):
            return True
        else:
            return False
