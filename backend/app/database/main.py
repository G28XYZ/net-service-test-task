from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import settings
from app.database.base import Base
from app.models.db import NetworkDB, NetworkInterfaceDB, VirtualMachineDB  # noqa: F401


async def async_main() -> None:
    # Проверяет подключение к PostgreSQL и при необходимости создает таблицы.
    engine = create_async_engine(settings.async_database_url, echo=True)
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        result = await conn.execute(text("select 'hello world'"))
        print(result.fetchall())
    await engine.dispose()
