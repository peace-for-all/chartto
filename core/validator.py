from string import punctuation

class Validator:
    def __init__(self):
        pass

    def check_token(self, api_token):
        """Returns true, if Todoist API token is valid"""
        for p in punctuation:
            if p in api_token:
                return False
        if not api_token:
            return False
        return True

    def check_username_exists(self, username):
        """Returns true, if username exists on the system"""
        pass

    def check_password_strong(self, password):
        """Returns true, if pass is strong, otherwise returns warning"""
        pass

    def check_password_matches(self, username, password):
        """Returns true, if password is correct for that user"""
        return True  # FIXME - it should be checked!

