from backend.role import Role
from backend.user import User

#adding the extra permissions into admin
class Admin(User):
    def __init__(self, user_id, username, password_hash, role=Role.User):
        super().__init__(user_id, username, password_hash, role)

    def add_watch(self, watch, catalogue):
        if not self.loggedin:
            raise PermissionError("Admin must be logged in before adding a watch")
        catalogue.add_watch(watch)