import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from tgbot.config import load_config
from tgbot.controllers.client_controller import fill_storage_by_clients
from tgbot.handlers.admin import admin_router
from tgbot.handlers.buttons import button_router
from tgbot.handlers.echo import echo_router
from tgbot.handlers.left_member import left_member_router
from tgbot.handlers.new_member import new_member_router
from tgbot.handlers.user_state import state_router
from tgbot.handlers.referral import referral_router
from tgbot.handlers.account import account_router
from tgbot.handlers.user import user_router
from tgbot.infrastructure.database.functions.setup import create_session_pool
from tgbot.middlewares.config import ConfigMiddleware
# from app_database import create_db_and_tables
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.services import broadcaster
from tgbot.services.rabbit.notification_receiver_queue import NotificationReceiverQueue

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
# create_db_and_tables()

async def on_startup(bot: Bot, admin_ids: list[int], loop, session):
    # create_db_and_tables()
    await fill_storage_by_clients(session)
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен")


def register_global_middlewares(dp: Dispatcher, config, session_pool):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))

    dp.message.outer_middleware(DatabaseMiddleware(session_pool))
    dp.callback_query.outer_middleware(DatabaseMiddleware(session_pool))
    dp.my_chat_member.outer_middleware(DatabaseMiddleware(session_pool))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    # if config.tg_bot.use_redis:
    #     storage = RedisStorage(config.redis.dsn(), key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True))
    # else:
    # create_jbot(create_engine(
    # config.db.uri(),
    # echo=True
    # ))
    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    session_pool = await create_session_pool(config.db, echo=False)

    for router in [
        new_member_router,
        left_member_router,
        admin_router,
        account_router,
        referral_router,
        user_router,
        button_router,
        state_router,
        echo_router
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, config, session_pool)
    loop = asyncio.get_event_loop()
    async with session_pool() as session:
        nr = NotificationReceiverQueue(bot, loop, session)

    await on_startup(bot, config.tg_bot.admin_ids, loop, session_pool)
    await nr.connect()
    task_nr = asyncio.create_task(nr.main())

    # await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member", "my_chat_member"])
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await  task_nr


if __name__ == '__main__':

    try:
        # create_db_and_tables()
        asyncio.run(main(), debug=True)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот был выключен!")
