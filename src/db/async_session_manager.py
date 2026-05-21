import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.conf import config
from src.logger.logger_config import logger

settings = config.DBSettings()
db_url = f'postgresql+psycopg://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}'


class Base(DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        logger.debug(f"Connecting to {host}")
        try:
            self._engine = create_async_engine(host, **engine_kwargs)
            self._sessionmaker = async_sessionmaker(bind=self._engine, expire_on_commit=False, class_=AsyncSession, autocommit=False)
            logger.info("✅ Database engine created successfully")
        except Exception as e:
            logger.exception(f"❌ Failed to create async engine: {e}")
            raise

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        logger.info("🔻 Closing database engine and sessionmaker")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None
        logger.info("✅ Database engine disposed successfully")

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        logger.debug("🔌 Opening async database connection")
        async with self._engine.begin() as connection:
            try:
                logger.debug("✅ Connection established successfully")
                yield connection
            except Exception as e:
                logger.error(f"⚠️ Error during connection: {e}, rolling back...")
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        logger.debug("🌀 Creating new async database session")
        session = self._sessionmaker()
        try:
            logger.debug("💾 Session completed successfully")
            yield session
        except Exception as e:
            logger.error(f"⚠️ Session error: {e}, performing rollback")
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.debug("🔒 Session closed")

sessionmanager = DatabaseSessionManager(db_url, {"echo": False, "pool_size": 100, "max_overflow": 0, "pool_pre_ping": True})

async def get_db_async_session() -> AsyncSession:
    logger.debug("🧩 Getting async DB session")
    async with sessionmanager.session() as session:
        yield session
    logger.debug("🧩 Session yielded and closed")
