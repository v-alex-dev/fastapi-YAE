from enum import Enum

class RoleEnum(str, Enum):
    """
    str + Enum → sérialisable en JSON automatiquement
    Stocké comme string en BDD
    """
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"
