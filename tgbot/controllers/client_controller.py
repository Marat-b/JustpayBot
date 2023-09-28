import logging

from tgbot.models.client_model import ClientDb
from tgbot.services.db.client_service import ClientDbService
from tgbot.services.redis.redis_storage import RedisStorage
from tgbot.utilz.payload_parser import payload_parser

logger = logging.getLogger(__name__)

def create_client(chat_id: int, text: str) -> ClientDb | None:
    """
    Create client from client handler
    :param chat_id: chat of client
    :type chat_id:
    :param text: hashed text
    :type text:
    :return:
    :rtype:
    """
    client = payload_parser(text)
    logger.info(f'client={client}')
    if 'customer_number' in client:
        client_service = ClientDbService()
        client = client_service.create(client['customer_id'], client['customer_number'], chat_id)
        return client
    else:
        return None

async def fill_storage_by_clients(loop):
    client_service = ClientDbService()
    clients = client_service.get_all_active_clients()
    selected_fields_clients = [{"client_id":client.chat_id, "customer_id":client.customer_id,"enable":client.enable} for
                               client in clients]
    logger.info(selected_fields_clients[0])
    rs = RedisStorage(loop)
    await rs.set(selected_fields_clients[0])
    # rs.close_con()


def set_client_enable_status(chat_id, status)->None:
    client_service = ClientDbService()
    client_service.set_enable_status(chat_id, status)

def is_client_exists(chat_id) -> bool:
    return ClientDbService().is_exists(chat_id)

