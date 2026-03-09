from enum import Enum
#creating the 2 different roles that the user can login to

class Role(Enum):
    User = "User"
    Admin = "Admin"