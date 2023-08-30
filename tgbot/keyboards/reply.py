from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# button1 = KeyboardButton(text='Как подключить уведомления?')
kb = [[KeyboardButton(text='Как подключить уведомления?'),
       KeyboardButton(text='Задать вопрос менеджеру')],
      [KeyboardButton(text='Решения для бизнеса от JustPay'),
       KeyboardButton(text='Внести предложение по улучшению сервиса')]]

menu = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
# menu.clean()
# menu.row(button1)