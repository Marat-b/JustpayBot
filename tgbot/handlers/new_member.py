from aiogram import Bot, F, Router
from aiogram.filters import ADMINISTRATOR, ChatMemberUpdatedFilter, IS_NOT_MEMBER, JOIN_TRANSITION, KICKED, LEFT, \
    MEMBER, \
    PROMOTED_TRANSITION, RESTRICTED
from aiogram.types import ChatMemberUpdated, Message

from tgbot.controllers.client_controller import set_client_enable_status
from tgbot.controllers.user_controller import set_user_enable_status
from tgbot.keyboards.reply import menu

new_member_router = Router()
# new_member_router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))
new_member_router.my_chat_member.filter(F.chat.type == "private")
new_member_router.message.filter(F.chat.type == "private")


# chats_variants = {
#     "group": "группу",
#     "supergroup": "супергруппу"
# }
#
#
# @new_member_router.my_chat_member(
#     ChatMemberUpdatedFilter(
#         member_status_changed=IS_NOT_MEMBER >> MEMBER
#     )
# )
# async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
#     # Вариант посложнее: бота добавили как обычного участника.
#     # Но может отсутствовать право написания сообщений, поэтому заранее проверим.
#     chat_info = await bot.get_chat(event.chat.id)
#     if chat_info.permissions.can_send_messages:
#         await bot.send_message(
#             chat_id=event.chat.id,
#             text=f"Привет! Спасибо, что добавили меня в "
#                  f'{chats_variants[event.chat.type]} "{event.chat.title}" '
#                  f"как обычного участника. ID чата: {event.chat.id}"
#         )
#     else:
#         print("Как-нибудь логируем эту ситуацию")


@new_member_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated, bot: Bot, session):
    # users.add(event.from_user.id)
    # write record to DB (event.from_user.id)
    print('Hello new member!!!')
    print(f'event.from_user.id={event.from_user.id}, event.chat.id={event.chat.id}')
    text = 'Вы успешно подписались на 👀 виртуального помощника компании JustPay.\n' \
 'Я буду присылать Вам уведомления 📧, которые Вы ' \
           'активировали в личном кабинете.\n Если у Вас остались вопросы, выберите пункт меню.👇'
    await set_client_enable_status(session, event.from_user.id, True)
    await set_user_enable_status(session, event.from_user.id, True)
    await bot.send_message(chat_id=event.chat.id,text=text, reply_markup=menu)

