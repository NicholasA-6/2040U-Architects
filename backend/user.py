from backend.role import role
# main user class

#creating the user class
class User:
    def __init__(self, user_id, username, password_hash, role = role.User):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.loggedin = False
    #checking if the user has logged into their respective account correctly
    def login(self, username, password):
        if self.username == username and self.password_hash == password:
            self.loggedin = True
            return True
        return False
    #logging out the user
    def logout(self):
        self.loggedin = False


    def is_loggedin(self):
        return self.loggedin