from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.keyboards.reply import menu

echo_router = Router()


@echo_router.message(F.text, StateFilter(None))
async def bot_echo(message: types.Message):
    text = [
        "Извините я Вас не понял 🤓",
        "Выберите пожалуйста нужный пункт меню или позвоните нам 8(800)33-33-175",

    ]

    await message.answer('\n'.join(text), reply_markup=menu)


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Ехо {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text), reply_markup=menu)

