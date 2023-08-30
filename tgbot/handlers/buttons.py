from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.misc.states import QuestionState, SuggestState

button_router = Router()

@button_router.message(F.text.lower() == 'как подключить уведомления?')
async def how_to(message: Message):
    text = ("1) Зайдите в свой Личный кабинет по адресу <a "
            "href='https://lk.justpay.pro/'>https://lk.justpay.pro/</a>\n2) Перейдите в пункт меню: "
            "<i>События-Настройка уведомлений</i>\n3) Отметьте уведомления в разделе <i>telegramm-bot</i>")
    await message.answer(text, parse_mode='HTML')

@button_router.message(F.text == 'Задать вопрос менеджеру')
async def ask_question(message: Message, state: FSMContext):
    await message.answer("Напишите вопрос и отправьте его:")
    await state.set_state(QuestionState.ask_question)
    # cfg = config.load_config('.env').mail
    # mail_sender = MailSender(cfg)
    # mail_sender.send_email('Test')


@button_router.message(F.text == 'Решения для бизнеса от JustPay')
async def business_task(message: Message):
    await message.answer("Решения для бизнеса от JustPay на сайте <a "
                        "href='https://justpay.pro/#solutions'>https://justpay.pro/#solutions</a>", parse_mode='HTML')

@button_router.message(F.text == 'Внести предложение по улучшению сервиса')
async def give_suggest(message: Message, state: FSMContext):
    await message.answer("Напишите предложение и отправьте его:")
    await state.set_state(SuggestState.give_suggest)

