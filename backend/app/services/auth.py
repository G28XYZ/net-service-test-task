class AuthService:
    _users = [
        {
            "id": 1,
            "username": "admin",
            "password": "admin",
            "role": "admin",
            "token": "dev-admin-token",
        }
    ]

    @classmethod
    def authenticate(cls, username: str, password: str) -> dict[str, str] | None:
        for user in cls._users:
            if user["username"] == username and user["password"] == password:
                return user
        return None

    @classmethod
    def get_user_by_token(cls, token: str) -> dict[str, str] | None:
        for user in cls._users:
            if user["token"] == token:
                return user
        return None

