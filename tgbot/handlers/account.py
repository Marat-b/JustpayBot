import logging

from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

account_router = Router()

@account_router.message(Command('account'))
async def referral(message: Message, bot: Bot, command: CommandObject):
    logging.info('*** account command ***')