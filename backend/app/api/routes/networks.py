from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.db import NetworkDB
from app.schemas.network import NetworkListResponse, NetworkResponse


router = APIRouter(prefix="/networks", tags=["networks"])


def serialize_network(network: NetworkDB) -> NetworkResponse:
    # Преобразует ORM-объект сети в ответ API.
    return NetworkResponse(
        id=network.id,
        name=network.name,
        status=network.status,
        createdAt=network.createdAt,
        cidr=network.cidr,
    )


@router.get("", response_model=NetworkListResponse)
async def list_networks(
    session: AsyncSession = Depends(get_db),
    _: dict[str, str] = Depends(get_current_user),
) -> NetworkListResponse:
    # Возвращает список доступных сетей.
    result = await session.execute(select(NetworkDB).order_by(NetworkDB.id))
    items = [serialize_network(network) for network in result.scalars().all()]
    return NetworkListResponse(items=items)
