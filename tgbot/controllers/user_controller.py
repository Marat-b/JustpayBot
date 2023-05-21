import json
import logging

from tgbot.models.user_model import UserDb
from tgbot.services.db.client_service import ClientDbService
from tgbot.services.db.user_service import UserDbService
# from tgbot.services.rabbit.account_message_queue import account_message
from tgbot.services.rabbit.participant_queue import ParticipantSender
from tgbot.utilz.payload_parser import payload_parser


def create_user(chat_id: int, text: str):
    user = payload_parser(text)
    print(f'user={user}')
    if 'participant_number' in user:
        print('Has attribute participant_number')
        user_service = UserDbService()
        user_service.create(user['client_id'], user['participant_number'], chat_id)
    if 'customer_number' in user:
        client_service = ClientDbService()
        client_service.create(user['client_id'], user['customer_number'], chat_id)

async def send_user(chat_id: int):
    user_service = UserDbService()
    user_message = user_service.to_str_by_chat_id(chat_id)
    if user_message is not None:
        user_sender = ParticipantSender()
        await user_sender.send(user_message)

# def get_account(str_accounts: str):
#     accounts = json.loads(str_accounts)
#     print(accounts)
#     if len(accounts) > 0:
#         account_messages = [account_message(account) for account in accounts]
#         print(account_messages)

def get_participant_by_chat_id_to_get_account(chat_id: int) -> str | None:
    user_service = UserDbService()
    user = user_service.get_by_chat_id(chat_id)
    if user is not None:
        return f'{{"company_id":"{user.company_id}","participant_number":"{user.participant_number}"}}'
    else:
        return None