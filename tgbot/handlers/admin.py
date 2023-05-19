import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart(deep_link=True))
async def admin_start(message: Message):
    await message.reply("Приветствую, админ!")
    await message.answer(message.text)
    logging.info(message.from_user.id)
