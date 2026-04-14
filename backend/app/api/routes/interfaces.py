from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_user, get_db
from app.models.db import NetworkDB, NetworkInterfaceDB, VirtualMachineDB
from app.schemas.interface import InterfaceCreateRequest, InterfaceListResponse, InterfaceResponse
from app.schemas.state import StatusChangeRequest


router = APIRouter(prefix="/interfaces", tags=["interfaces"])


def serialize_interface(interface: NetworkInterfaceDB) -> InterfaceResponse:
    # Преобразует ORM-объект интерфейса в ответ API.
    return InterfaceResponse(
        id=interface.id,
        name=interface.name,
        status=interface.status,
        createdAt=interface.createdAt,
        vmId=interface.vmId,
        networkId=interface.networkId,
    )


async def get_vm(session: AsyncSession, vm_id: int) -> VirtualMachineDB | None:
    # Нужен для валидации привязки интерфейса к существующей ВМ.
    result = await session.execute(
        select(VirtualMachineDB)
        .options(selectinload(VirtualMachineDB.interfaces))
        .where(VirtualMachineDB.id == vm_id)
    )
    return result.scalar_one_or_none()


@router.get("", response_model=InterfaceListResponse)
async def list_interfaces(
    session: AsyncSession = Depends(get_db),
    _: dict[str, str] = Depends(get_current_user),
) -> InterfaceListResponse:
    # Возвращает список всех сетевых интерфейсов.
    result = await session.execute(select(NetworkInterfaceDB).order_by(NetworkInterfaceDB.id))
    items = [serialize_interface(interface) for interface in result.scalars().all()]
    return InterfaceListResponse(items=items)


@router.post("", response_model=InterfaceResponse, status_code=status.HTTP_201_CREATED)
async def create_interface(
    payload: InterfaceCreateRequest,
    session: AsyncSession = Depends(get_db),
    _: dict[str, str] = Depends(get_current_user),
) -> InterfaceResponse:
    # Создает интерфейс только если существуют и ВМ, и сеть.
    vm = await get_vm(session, payload.vmId)
    if vm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual machine not found.",
        )

    network = await session.get(NetworkDB, payload.networkId)
    if network is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Network not found.",
        )

    interface = NetworkInterfaceDB(
        name=payload.name,
        status="down",
        createdAt=datetime.now(UTC),
        vmId=payload.vmId,
        networkId=payload.networkId,
    )
    session.add(interface)
    await session.commit()
    await session.refresh(interface)
    return serialize_interface(interface)


@router.patch("/{interface_id}/status", response_model=InterfaceResponse)
async def change_interface_status(
    interface_id: int,
    payload: StatusChangeRequest,
    session: AsyncSession = Depends(get_db),
    _: dict[str, str] = Depends(get_current_user),
) -> InterfaceResponse:
    # Заготовка под тестовое задание: переключение состояния интерфейса.
    interface = await session.get(NetworkInterfaceDB, interface_id)
    if interface is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interface not found.",
        )

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Test task: реализовать обработчик состояния интерфейса. "
            f"Requested status: {payload.status}."
        ),
    )
