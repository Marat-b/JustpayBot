from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.methods import SendContact
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from tgbot.controllers.user_controller import create_user, send_user
from tgbot.keyboards.reply import menu
from tgbot.utilz.payload_parser import payload_parser

user_router = Router()

text =['Привет {}👋',
       '👀 Я виртуальный помощник компании JustPay',
       'Я ещё многому учусь, но уже умею присылать важную информацию по точкам продажам 😎:',
       "✔ сводный отчёт по продажам за день",
       "✔ экстренные сообщения: если был возврат, не прошла сверка итогов, были ошибки в платежах",
       "✔ фискальные чеки по точкам",
       "",
       "А ещё могу предложить бизнес решения нашей компании, ответить на вопросы по подключению эквайринга и покупке "
       "терминала. Для этого Вам необходимо нажать кнопку подписаться"]

@user_router.message(CommandStart())
async def user_start(message: Message):
    print(f'text={message.text}')
    message_texts = message.text

    text_splitted = message_texts.split(' ') # split from 'start <hashed text>'

    if len(text_splitted)==2:
        create_user(message.from_user.id, decode_payload(text_splitted[1]))

        # send user data to message queuue
        # await send_user(message.from_user.id)
    else:
        fio = f'{message.from_user.first_name} {message.from_user.last_name}'
        await message.answer(('\n'.join(text)).format(fio), reply_markup=menu)
