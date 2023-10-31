from typing import Callable, AsyncGenerator, AsyncContextManager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import DbConfig
# from tgbot.infrastructure.database.models.base import DatabaseModel

from tgbot.models.get_base import Base


async def create_session_pool(db: DbConfig, echo=False) -> Callable[[], AsyncContextManager[AsyncSession]]:
    engine = create_async_engine(
        db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=10,
        max_overflow=200,
        future=True,
        echo=echo,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # await conn.run_sync(DatabaseModel.metadata.create_all)

    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool