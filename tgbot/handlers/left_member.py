from aiogram import Bot, F, Router
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER
from aiogram.types import ChatMemberUpdated, Message

from tgbot.controllers.client_controller import set_client_enable_status
from tgbot.controllers.user_controller import set_user_enable_status

left_member_router = Router()

left_member_router.my_chat_member.filter(F.chat.type == "private")
left_member_router.message.filter(F.chat.type == "private")

@left_member_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER >> IS_NOT_MEMBER)
)
async def user_blocked_bot(event: ChatMemberUpdated, bot: Bot):
    # users.add(event.from_user.id)
    # write record to DB (event.from_user.id)
    print('Good buy old member!!!')
    print(f'event.from_user.id={event.from_user.id}, event.chat.id={event.chat.id}')
    # text = 'Вы успешно отписались на виртуального помощника JustPay.Если вы случайно отписались нажмите кнопку.'
    # await bot.send_message(chat_id=event.chat.id,text=text)
    # await message.answer(text)
    set_client_enable_status(event.from_user.id, False)
    set_user_enable_status(event.from_user.id, False)

