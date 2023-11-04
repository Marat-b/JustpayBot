from contextlib import asynccontextmanager
from typing import Callable, AsyncGenerator, AsyncContextManager

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from tgbot.config import DbConfig, load_config
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

config = load_config(".env")
def create_engine():
    engine = create_async_engine(
        config.db.construct_sqlalchemy_url(),
        # query_cache_size=1200,
        # pool_size=10,
        # max_overflow=200,
        # future=True,
        echo=True,
        poolclass=NullPool,
    )
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    return engine

engine = create_engine()

# @asynccontextmanager
async def get_session(echo=False):

    # async with session_pool() as session:
        # async_session: AsyncSession = session
    # try:
        # engine = create_async_engine(
        #     db.construct_sqlalchemy_url(),
        #     # query_cache_size=1200,
        #     # pool_size=10,
        #     # max_overflow=200,
        #     # future=True,
        #     echo=echo,
        #     poolclass=NullPool,
        # )
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.create_all)

    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with session_pool() as async_session:
        # async  with async_session.begin():
        return  async_session
    # finally:
    #     print('finally get_session. Before close')
    #     await async_session.close()
    #     print('finally get_session. After close')
