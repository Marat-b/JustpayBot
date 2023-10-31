from aiogram import Bot, Router
from aiogram.client import bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Chat, ChatInviteLink, Message, User
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hcode
from aiogram.methods import CreateChatInviteLink

from tgbot.services.db.client_service import ClientDbService

referral_router = Router()

@referral_router.message(Command('referral'))
async def referral(message: Message, bot: Bot, command: CommandObject, session):
    # start_link_encoded = await get_start_link(message.from_user.id, encode=True)
    chat_id = message.chat.id
    # print(f'bot.id={chat_id}')
    client_service = ClientDbService(session)
    customers = await client_service.get_by_chat_id(chat_id)
    # print(f'payload={customer.customer_id}')
    # TODO must be one record with customer
    if len(customers) > 0:
        start_link_encoded = await create_start_link(bot, f'c{customers[0].customer_id}',
                                                     encode=True)
        # print(start_link_encoded)
        await message.answer(f'Скопируйте ссылку и отправьте её выбранному пользователю <b>{hcode(start_link_encoded)}</b>')
    else:
        await message.answer('Пользователь не найден')
    # chat: User = await bot.get_me()
    # result: Chat = await bot.get_chat(chat.id)
    # result: ChatInviteLink = await bot.create_chat_invite_link(chat.id)
    # print(result)
