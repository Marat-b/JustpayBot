from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.methods import SendContact
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from tgbot.utilz.payload_parser import payload_parser

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Приветствую, обычный пользователь!")
    await message.answer(f'user id {message.from_user.id}')
    print('User answered')
    await message.answer(message.text)
    print(f'text={message.text}')
    message_texts = message.text

    text_splitted = message_texts.split(' ')

    # payloads = payload_parser(decode_payload(text_splitted[1]))
    payloads = payload_parser(text_splitted[1])
    print(f'payloads={payloads}')
    print(f'payloads[0]={payloads["customer_id"]}')

    # if len(text_splitted)==2:
    #     decoded_text = decode_payload(text_splitted[1])
    #     # decoded_text = text_splitted[1]
    #     print(f'decoded_text={decoded_text}')
    #     participant_id, participant_number = decoded_text.split('_')
    #     print(f'participant_id={participant_id}, participant_number={participant_number}')
        # write record to DB (participant_id, participant_number) with the appropriate chatId

    # result = await SendContact(chat_id=message.from_user.id)
    # await message.answer(message.contact.phone_number)
