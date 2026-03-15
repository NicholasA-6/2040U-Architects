from enum import Enum
#creating the 2 different roles that the user can login to

class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"