from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.db import NetworkDB, NetworkInterfaceDB, VirtualMachineDB
from app.schemas.interface import InterfaceCreateRequest, InterfaceResponse
from app.schemas.network import NetworkResponse
from app.schemas.vm import VirtualMachineCreateRequest, VirtualMachineResponse


class InventoryService:
    """Сервисный слой для чтения и изменения сетей, ВМ и интерфейсов в БД."""

    @staticmethod
    def _serialize_vm(vm: VirtualMachineDB) -> VirtualMachineResponse:
        """Преобразует ORM-модель ВМ в API-схему ответа."""
        network_ids = sorted({interface.networkId for interface in vm.interfaces})
        return VirtualMachineResponse(
            id=vm.id,
            name=vm.name,
            status=vm.status,
            createdAt=vm.createdAt,
            networkIds=network_ids,
        )

    @staticmethod
    def _serialize_interface(interface: NetworkInterfaceDB) -> InterfaceResponse:
        """Преобразует ORM-модель интерфейса в API-схему ответа."""
        return InterfaceResponse(
            id=interface.id,
            name=interface.name,
            status=interface.status,
            createdAt=interface.createdAt,
            vmId=interface.vmId,
            networkId=interface.networkId,
        )

    @staticmethod
    def _serialize_network(network: NetworkDB) -> NetworkResponse:
        """Преобразует ORM-модель сети в API-схему ответа."""
        return NetworkResponse(
            id=network.id,
            name=network.name,
            status=network.status,
            createdAt=network.createdAt,
            cidr=network.cidr,
        )

    @classmethod
    async def list_networks(cls, session: AsyncSession) -> list[NetworkResponse]:
        """Возвращает список всех сетей из базы данных."""
        result = await session.execute(select(NetworkDB).order_by(NetworkDB.id))
        return [cls._serialize_network(network) for network in result.scalars().all()]

    @classmethod
    async def get_network(cls, session: AsyncSession, network_id: int) -> NetworkDB | None:
        """Ищет сеть по идентификатору."""
        return await session.get(NetworkDB, network_id)

    @classmethod
    async def list_virtual_machines(cls, session: AsyncSession) -> list[VirtualMachineResponse]:
        """Возвращает список всех ВМ вместе с их интерфейсами."""
        result = await session.execute(
            select(VirtualMachineDB)
            .options(selectinload(VirtualMachineDB.interfaces))
            .order_by(VirtualMachineDB.id)
        )
        return [cls._serialize_vm(vm) for vm in result.scalars().all()]

    @classmethod
    async def get_virtual_machine(cls, session: AsyncSession, vm_id: int) -> VirtualMachineDB | None:
        """Ищет ВМ по идентификатору и загружает связанные интерфейсы."""
        result = await session.execute(
            select(VirtualMachineDB)
            .options(selectinload(VirtualMachineDB.interfaces))
            .where(VirtualMachineDB.id == vm_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def create_virtual_machine(
        cls,
        session: AsyncSession,
        payload: VirtualMachineCreateRequest,
    ) -> VirtualMachineResponse:
        """Создает новую виртуальную машину со статусом stopped."""
        vm = VirtualMachineDB(
            name=payload.name,
            status="stopped",
            createdAt=datetime.now(UTC),
        )
        session.add(vm)
        await session.commit()
        await session.refresh(vm)
        await session.refresh(vm, attribute_names=["interfaces"])
        return cls._serialize_vm(vm)

    @classmethod
    async def create_interface(
        cls,
        session: AsyncSession,
        payload: InterfaceCreateRequest,
    ) -> InterfaceResponse:
        """Создает новый сетевой интерфейс для выбранной ВМ и сети."""
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
        return cls._serialize_interface(interface)

    @classmethod
    async def list_interfaces(cls, session: AsyncSession) -> list[InterfaceResponse]:
        """Возвращает список всех сетевых интерфейсов."""
        result = await session.execute(select(NetworkInterfaceDB).order_by(NetworkInterfaceDB.id))
        return [cls._serialize_interface(interface) for interface in result.scalars().all()]

    @classmethod
    async def change_virtual_machine_status(
        cls,
        session: AsyncSession,
        vm_id: int,
        next_status: str,
    ) -> VirtualMachineResponse:
        """Проверяет существование ВМ и оставляет обработку статуса как часть тестового задания."""
        vm = await cls.get_virtual_machine(session, vm_id)
        if vm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Virtual machine not found.",
            )

        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=(
                "Test task: реализовать обработчик состояния виртуальной машины."
                f"Requested status: {next_status}."
            ),
        )

    @classmethod
    async def change_interface_status(
        cls,
        session: AsyncSession,
        interface_id: int,
        next_status: str,
    ) -> InterfaceResponse:
        """Проверяет существование интерфейса и оставляет смену статуса как часть тестового задания."""
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
                f"Requested status: {next_status}."
            ),
        )

    @classmethod
    async def delete_virtual_machine(cls, session: AsyncSession, vm_id: int) -> None:
        """Удаляет ВМ по идентификатору вместе со связанными интерфейсами."""
        vm = await cls.get_virtual_machine(session, vm_id)
        if vm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Virtual machine not found.",
            )

        await session.delete(vm)
        await session.commit()
