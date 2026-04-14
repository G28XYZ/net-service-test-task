from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings


engine = create_async_engine(settings.async_database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    # Создает сессию на время одного запроса и закрывает ее после завершения.
    async with AsyncSessionLocal() as session:
        yield session
