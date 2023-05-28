import json
import logging

from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from tgbot.controllers.user_controller import get_participant_by_chat_id_to_get_account
from tgbot.services.rabbit.account_message_queue import AccountMessageRpcClient

account_router = Router()

def account_message(account_dict) -> str:
    text = "Счёт:\t{}\nНазвание счёта:\t{}\nОписание счёта:\t{}\nСумма на счёте\t{}\nСчёт создан\t{}".format(
        account_dict["account"],account_dict["campaign_name"],account_dict["campaign_description"],account_dict["amount"],
        account_dict["campaign_create_date"]
    )
    return text
@account_router.message(Command('account'))
async def account(message: Message, bot: Bot, command: CommandObject):
    logging.info('*** account command ***')
    user_data = get_participant_by_chat_id_to_get_account(message.from_user.id)
    # user_data = get_participant_by_chat_id_to_get_account(0)
    if user_data is not None:
        account_message_rpc = await AccountMessageRpcClient().connect()
        # send request to message queue
        response = await account_message_rpc.call(user_data)
        print(f" [.] Got {response}")
        accounts = json.loads(response)
        logging.info(accounts)
        for account in accounts:
            # logging.info(account_message(account))
            await message.answer(account_message(account))
    else:
        await message.answer('Данные не найдены')