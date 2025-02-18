from models.Enums import Role


class User:
    def __init__(self, username: str, password: str, role: Role):
        self.username = username
        self.password = password  # À hasher
        self.role = role
