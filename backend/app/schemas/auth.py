from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Схема запроса на авторизацию пользователя."""

    # Логин пользователя для входа в систему.
    username: str
    # Пароль пользователя для входа в систему.
    password: str


class LoginResponse(BaseModel):
    """Схема успешного ответа после авторизации."""

    # Bearer-токен для последующих запросов к API.
    accessToken: str
    # Имя пользователя, от имени которого открыта сессия.
    username: str
    # Роль пользователя в системе.
    role: str
