from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_user, get_db
from app.models.db import VirtualMachineDB
from app.schemas.state import StatusChangeRequest
from app.schemas.vm import VirtualMachineCreateRequest, VirtualMachineListResponse, VirtualMachineResponse


router = APIRouter(prefix="/virtual-machines", tags=["virtual-machines"])


def serialize_vm(vm: VirtualMachineDB) -> VirtualMachineResponse:
    # Собирает API-ответ ВМ вместе со списком связанных сетей.
    network_ids = sorted({interface.networkId for interface in vm.interfaces})
    return VirtualMachineResponse(
        id=vm.id,
        name=vm.name,
        status=vm.status,
        createdAt=vm.createdAt,
        networkIds=network_ids,
    )


async def get_vm(session: AsyncSession, vm_id: int) -> VirtualMachineDB | None:
    # Загружает ВМ вместе с интерфейсами, чтобы не делать повторные запросы.
    result = await session.execute(
        select(VirtualMachineDB)
        .options(selectinload(VirtualMachineDB.interfaces))
        .where(VirtualMachineDB.id == vm_id)
    )
    return result.scalar_one_or_none()


@router.get("", response_model=VirtualMachineListResponse)
async def list_virtual_machines(
    session: AsyncSession = Depends(get_db),
    _: dict[str, str] = Depends(get_current_user),
) -> VirtualMachineListResponse:
    # Возвращает список всех виртуальных машин.
    result = await session.execute(
        select(VirtualMachineDB)
        .options(selectinload(VirtualMachineDB.interfaces))
        .order_by(VirtualMachineDB.id)
    )
    items = [serialize_vm(vm) for vm in result.scalars().all()]
    return VirtualMachineListResponse(items=items)


@router.post("", response_model=VirtualMachineResponse)
async def create_virtual_machine(
    payload: VirtualMachineCreateRequest,
    session: AsyncSession = Depends(get_db),
    _: dict[str, str] = Depends(get_current_user),
) -> VirtualMachineResponse:
    # Создает новую ВМ со статусом stopped.
    vm = VirtualMachineDB(
        name=payload.name,
        status="stopped",
        createdAt=datetime.now(UTC),
    )
    session.add(vm)
    await session.commit()
    await session.refresh(vm)
    await session.refresh(vm, attribute_names=["interfaces"])
    return serialize_vm(vm)


@router.patch("/{vm_id}/status", response_model=VirtualMachineResponse)
async def change_virtual_machine_status(
    vm_id: int,
    payload: StatusChangeRequest,
    session: AsyncSession = Depends(get_db),
    _: dict[str, str] = Depends(get_current_user),
) -> VirtualMachineResponse:
    # Заготовка под тестовое задание: переключение состояния ВМ.
    vm = await get_vm(session, vm_id)
    if vm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual machine not found.",
        )

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Test task: реализовать обработчик состояния виртуальной машины."
            f"Requested status: {payload.status}."
        ),
    )


@router.delete("/{vm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_virtual_machine(
    vm_id: int,
    session: AsyncSession = Depends(get_db),
    _: dict[str, str] = Depends(get_current_user),
) -> Response:
    # Удаляет ВМ и связанные с ней интерфейсы через ORM cascade.
    vm = await get_vm(session, vm_id)
    if vm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual machine not found.",
        )

    await session.delete(vm)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
