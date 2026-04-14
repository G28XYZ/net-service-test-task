from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest) -> LoginResponse:
    # Возвращает демо-токен для заранее заданного пользователя.
    user = AuthService.authenticate(payload.username, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    return LoginResponse(
        accessToken=user["token"],
        username=user["username"],
        role=user["role"],
    )
