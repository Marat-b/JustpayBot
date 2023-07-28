import json
import logging

from aiogram import Bot

from tgbot.models.user_model import UserDb
from tgbot.services.db.client_service import ClientDbService
from tgbot.services.db.user_service import UserDbService
# from tgbot.services.rabbit.account_message_queue import account_message
from tgbot.services.rabbit.participant_queue import ParticipantSender
from tgbot.utilz.payload_parser import payload_parser


def create_user(chat_id: int, text: str):
    """
    Create user from user handler
    :param chat_id: chat of user
    :type chat_id:
    :param text: hashed text
    :type text:
    :return:
    :rtype:
    """
    user = payload_parser(text)
    print(f'user={user}')
    if 'participant_number' in user:
        print('Has attribute participant_number')
        user_service = UserDbService()
        user_service.create(user['client_id'], user['participant_number'], chat_id)
    if 'customer_number' in user:
        client_service = ClientDbService()
        client_service.create(user['customer_id'], user['customer_number'], chat_id)


async def send_user(chat_id: int):
    """
    Send user data to Message queue
    :param chat_id:
    :type int:
    :return:
    :rtype:
    """
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


def get_chat_id_by_company_id_to_get_account(company_id: str, participant_number: int) -> str | None:
    user_service = UserDbService()
    user = user_service.get_by_company_id_participant_number(company_id, participant_number)
    return user.chat_id if user is not None else None

def get_chat_id_by_customer_id(customer_id: str) -> int | None:
    client_service = ClientDbService()
    chat_id = client_service.get_chat_id_by_customer_id(customer_id)
    return chat_id


async def send_message(bot: Bot, record) -> None:
    """
    Send message to user from queue.
    :param bot: Bot
    :param records: Dictionary
    :return: None
    """

    # company_id: str, participant_number: int, title: str, text: str = None
    chat_id = get_chat_id_by_company_id_to_get_account(record["initiator"], record["receiver"])
    logging.info(f'chat_id={chat_id}')
    if chat_id is not None:
        if record["content"] is None:
            await bot.send_message(chat_id=chat_id, text=record["name"])
        else:
            await bot.send_message(
                chat_id=chat_id, text="<b>{}</b>\n{}".format(record["name"],record["content"]),
                parse_mode='HTML'
                )

async def send_message_to_customer(bot: Bot, record) -> None:
    """
    Send message to customer from queue.
    :param bot: Bot
    :param records: Dictionary
    :return: None
    """

    # company_id: str, participant_number: int, title: str, text: str = None
    print(record["receiver"])
    chat_id = get_chat_id_by_customer_id(record["receiver"])
    # chat_id = 147166708
    logging.info(f'chat_id={chat_id}')
    if chat_id is not None:
        if record["content"] is None:
            await bot.send_message(chat_id=chat_id, text=record["name"])
        else:
            await bot.send_message(
                chat_id=chat_id, text="<b>{}</b>\n{}".format(record["name"],record["content"]),
                parse_mode='HTML'
                )
