from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.services.auth import AuthService


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, str]:
    # Проверяет Bearer-токен и возвращает текущего пользователя.
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    user = AuthService.get_user_by_token(credentials.credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    return user


async def get_db(credentials: AsyncSession = Depends(get_db_session)) -> AsyncSession:
    # Прокидывает активную сессию БД в обработчики FastAPI.
    return credentials
