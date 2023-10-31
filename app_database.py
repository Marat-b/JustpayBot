import asyncio

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_session
from sqlalchemy.orm import Session

from tgbot.config import load_config
from tgbot.infrastructure.database.functions.setup import create_session_pool
from tgbot.models.client_model import Base

config = load_config(".env")

engine = create_engine(
    config.db.uri(),
)


def create_db_and_tables():
    Base.metadata.create_all(engine)


# def create_jbot(engin):
#     SQLModel.metadata.create_all(engin)
#     pass

# def get_session():
#     with Session(engine) as session:
#         yield session

# async def get_session() -> AsyncSession:
#     async with create_session_pool(load_config(".env").db) as session:
#         yield session
#
#
# def run_and_get(coro):
#     task = asyncio.create_task(coro)
#     asyncio.get_running_loop().run_until_complete(task)
#     return task.result()
#
#
# class AsyncObj:
#     def __init__(self, *args, **kwargs):
#         """
#         Standard constructor used for arguments pass
#         Do not override. Use __ainit__ instead
#         """
#         self.__storedargs = args, kwargs
#         self.async_initialized = False
#
#     async def __ainit__(self, *args, **kwargs):
#         """ Async constructor, you should implement this """
#
#     async def __initobj(self):
#         """ Crutch used for __await__ after spawning """
#         assert not self.async_initialized
#         self.async_initialized = True
#         await self.__ainit__(
#             *self.__storedargs[0], **self.__storedargs[1]
#             )  # pass the parameters to __ainit__ that passed to __init__
#         return self
#
#     def __await__(self):
#         return self.__initobj().__await__()
#
#     def __init_subclass__(cls, **kwargs):
#         assert asyncio.iscoroutinefunction(cls.__ainit__)  # __ainit__ must be async
#
#     @property
#     def async_state(self):
#         if not self.async_initialized:
#             return "[initialization pending]"
#         return "[initialization done and successful]"
