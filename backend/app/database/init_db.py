from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base
from app.database.session import engine
from app.models.db import NetworkDB, NetworkInterfaceDB, VirtualMachineDB


async def init_db() -> None:
    # Создает таблицы и один раз заполняет БД демо-данными.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        await seed_data(session)


async def seed_data(session: AsyncSession) -> None:
    # Не дублирует сиды, если в таблице сетей уже есть записи.
    existing_network = await session.execute(select(NetworkDB.id).limit(1))
    if existing_network.scalar_one_or_none() is not None:
        return

    public_net = NetworkDB(
        name="public-net",
        status="active",
        createdAt=datetime(2026, 4, 10, 9, 0, tzinfo=UTC),
        cidr="10.10.0.0/24",
    )
    private_net = NetworkDB(
        name="private-net",
        status="active",
        createdAt=datetime(2026, 4, 10, 10, 0, tzinfo=UTC),
        cidr="10.20.0.0/24",
    )
    session.add_all([public_net, private_net])
    await session.flush()

    vm_app = VirtualMachineDB(
        name="vm-app-01",
        status="running",
        createdAt=datetime(2026, 4, 11, 12, 0, tzinfo=UTC),
    )
    vm_db = VirtualMachineDB(
        name="vm-db-01",
        status="stopped",
        createdAt=datetime(2026, 4, 11, 12, 30, tzinfo=UTC),
    )
    session.add_all([vm_app, vm_db])
    await session.flush()

    session.add_all(
        [
            NetworkInterfaceDB(
                name="eth0",
                status="up",
                createdAt=datetime(2026, 4, 11, 12, 5, tzinfo=UTC),
                vmId=vm_app.id,
                networkId=public_net.id,
            ),
            NetworkInterfaceDB(
                name="eth1",
                status="down",
                createdAt=datetime(2026, 4, 11, 12, 35, tzinfo=UTC),
                vmId=vm_db.id,
                networkId=private_net.id,
            ),
        ]
    )
    await session.commit()
