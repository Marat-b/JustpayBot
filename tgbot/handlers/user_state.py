from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import menu
from tgbot.misc.states import QuestionState, SuggestState
from tgbot.services.mail_sender import send_email

state_router = Router()
@state_router.message(QuestionState.ask_question)
async def ask_question(message: Message, state: FSMContext):
    print(message.chat.full_name)
    await message.answer(text="Спасибо за вопрос! Сообщение отправлено.", reply_markup=menu)
    await state.clear()
    await send_email("Вопрос менеджеру от {} ({})".format(message.chat.full_name, message.chat.username), message.text)

@state_router.message(SuggestState.give_suggest)
async def ask_question(message: Message, state: FSMContext):
    print(message.chat.full_name)
    await message.answer(text="Спасибо за предложение! Сообщение отправлено.", reply_markup=menu)
    await state.clear()
    await send_email("Предложение по бизнесу от {} ({})".format(message.chat.full_name, message.chat.username),
                     message.text)