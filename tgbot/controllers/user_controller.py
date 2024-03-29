import asyncio
import json
import logging
from typing import List

from aiogram import Bot

from tgbot.infrastructure.database.functions.setup import get_session
from tgbot.models.client_model import ClientDb
from tgbot.models.user_model import UserDb
from tgbot.services.db.client_service import ClientDbService
from tgbot.services.db.user_service import UserDbService
from tgbot.services.rabbit.participant_queue import ParticipantSender
from tgbot.utilz.payload_parser import payload_parser

logger = logging.getLogger(__name__)

async def create_user(chat_id: int, text: str):
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
    logger.info(f'user={user}')
    if 'participant_number' in user:
        logger.info('Has attribute participant_number')
        session = await get_session()
        user_service = UserDbService(session)
        await user_service.create(user['participant_number'], chat_id)
    # if 'customer_number' in user:
    #     client_service = ClientDbService()
    #     client_service.create(user['customer_id'], user['customer_number'], chat_id)


async def send_user(chat_id: int):
    """
    Send user data to Message queue
    :param chat_id:
    :type int:
    :return:
    :rtype:
    """
    session = await get_session()
    user_service = UserDbService(session)
    user_message = await user_service.to_str_by_chat_id(chat_id)
    if user_message is not None:
        user_sender = ParticipantSender()
        await user_sender.send(user_message)

async def is_user_exists( chat_id) -> bool:
    session = await get_session()
    result =  await UserDbService(session).is_exists(chat_id)
    return result

# def get_account(str_accounts: str):
#     accounts = json.loads(str_accounts)
#     logger.info(accounts)
#     if len(accounts) > 0:
#         account_messages = [account_message(account) for account in accounts]
#         logger.info(account_messages)

async def get_participant_by_chat_id_to_get_account(chat_id: int) -> str | None:
    session = await get_session()
    user_service = UserDbService(session)
    user = await user_service.get_by_chat_id(chat_id)
    if user is not None:
        return f'{{"company_id":"{user.company_id}","participant_number":"{user.participant_number}"}}'
    else:
        return None


async def get_chat_id_by_company_id_to_get_account(company_id: str, participant_number: int) -> str | None:
    session = await get_session()
    user_service = UserDbService(session)
    user = await user_service.get_by_company_id_participant_number(company_id, participant_number)
    return user.chat_id if user is not None else None

async def get_chat_id_by_customer_id(customer_id: str) -> List[int]:
    """
    Get list of chat id by customer id
    :param customer_id:
    :type customer_id:
    :return:
    :rtype:
    """
    session = await get_session()
    client_service = ClientDbService(session)
    chat_ids = await client_service.get_chat_id_by_customer_id(customer_id)
    return chat_ids

async def get_chat_id_by_participant_number(participant_number: int) -> int:
    session = await get_session()
    user_service = UserDbService(session)
    user = await user_service.get_by_number(participant_number)
    return user.chat_id if user is not None else None

async def send_message(bot: Bot, record) -> None:
    """
    Send message to user from queue.
    :param bot: Bot
    :param records: Dictionary
    :return: None
    """

    # company_id: str, participant_number: int, title: str, text: str = None
    # chat_id = get_chat_id_by_company_id_to_get_account(record["initiator"], record["receiver"])
    receivers = record["receiver"].split(';')
    for receiver in receivers:
        chat_id = await get_chat_id_by_participant_number(int(receiver))
        logger.info(f'chat_id={chat_id}')
        if chat_id is not None:
            if record["content"] is None:
                await bot.send_message(chat_id=chat_id, text=record["name"])
            else:
                await bot.send_message(
                    chat_id=chat_id, text="<b>{}</b>\n{}".format(record["name"],record["content"]),
                    parse_mode='HTML'
                    )
            await asyncio.sleep(0.05) # 20 messages per second (Limit: 30 messages per second)

async def send_message_to_customer(bot: Bot, record) -> None:
    """
    Send message to customer from queue.
    :param bot: Bot
    :param records: Dictionary
    :return: None
    """
    try:
        # company_id: str, participant_number: int, title: str, text: str = None
        logger.info(record["receiver"])
        chat_ids = await get_chat_id_by_customer_id(record["receiver"])
        # chat_id = 147166708
        for chat_id in chat_ids:
            logger.info(f'chat_id={chat_id}')
            if record["content"] is None:
                await bot.send_message(chat_id=chat_id, text=record["name"])
            else:
                await bot.send_message(
                    chat_id=chat_id, text="<b>{}</b>\n{}".format(record["name"],record["content"]),
                    parse_mode='HTML'
                    )
            await asyncio.sleep(0.05)
    except Exception as e:
        logging.error(f'Exception={e}')


async def set_user_enable_status(chat_id, status)->None:
    session = await get_session()
    user_service = UserDbService(session)
    await user_service.set_enable_status(chat_id, status)