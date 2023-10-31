import logging

from tgbot.models.client_model import ClientDb
from tgbot.services.db.client_service import ClientDbService
from tgbot.services.redis.redis_storage import RedisStorage
from tgbot.utilz.payload_parser import payload_parser

logger = logging.getLogger(__name__)

async def create_client(session, chat_id: int, text: str) -> ClientDb | None:
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
        client_service = ClientDbService(session)
        client = await client_service.create(client['customer_id'], client['customer_number'], chat_id)
        set_client_to_redis(client)
        return client
    else:
        return None

async def fill_storage_by_clients(session_pool):
    async with session_pool() as session:
        client_service = ClientDbService(session)
        clients = await client_service.get_all_active_clients()
        # for client in clients:
        #     print(client)
        set_clients_to_redis(clients)

async def set_client_enable_status(session, chat_id, status)->None:
    client_service = ClientDbService(session)
    clients = await client_service.set_enable_status(chat_id, status)
    set_clients_to_redis(clients)

def set_client_to_redis(client: ClientDb):
    if client is not None:
        selected_fields_client = {"chat_id": client.chat_id, "customer_id": client.customer_id, "enable":
            client.enable}
        logger.info(selected_fields_client)
        rs = RedisStorage()
        rs.set(selected_fields_client)
        rs.close_con()

def set_clients_to_redis(clients: list[ClientDb]):
    selected_fields_clients = [{"chat_id": client.chat_id, "customer_id": client.customer_id, "enable": client.enable}
                               for  client in clients]
    # logger.info(selected_fields_clients[0])
    rs = RedisStorage()
    # rs.remove()
    rs.set_list(selected_fields_clients)
    rs.close_con()

async def is_client_exists(session, chat_id) -> bool:
    result = await ClientDbService(session).is_exists(chat_id)
    return result

