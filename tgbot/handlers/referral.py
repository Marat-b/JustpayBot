from aiogram import Bot, Router
from aiogram.client import bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Chat, ChatInviteLink, Message, User
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hcode
from aiogram.methods import CreateChatInviteLink



referral_router = Router()

@referral_router.message(Command('referral'))
async def referral(message: Message, bot: Bot, command: CommandObject):
    # start_link_encoded = await get_start_link(message.from_user.id, encode=True)
    start_link_encoded = await create_start_link(bot, '6167e0eccf10537f879b0f73_1009', encode=True)
    print(start_link_encoded)
    await message.answer(f'Скопируйте ссылку и отправьте её выбранному пользователю <b>{hcode(start_link_encoded)}</b>')
    # chat: User = await bot.get_me()
    # result: Chat = await bot.get_chat(chat.id)
    # result: ChatInviteLink = await bot.create_chat_invite_link(chat.id)
    # print(result)
