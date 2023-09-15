from tgbot.models.client_model import ClientDb
from tgbot.services.db.client_service import ClientDbService
from tgbot.utilz.payload_parser import payload_parser


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
    print(f'client={client}')
    if 'customer_number' in client:
        client_service = ClientDbService()
        client = client_service.create(client['customer_id'], client['customer_number'], chat_id)
        return client
    else:
        return None

def set_client_enable_status(chat_id, status)->None:
    client_service = ClientDbService()
    client_service.set_enable_status(chat_id, status)

def is_client_exists(chat_id) -> bool:
    return ClientDbService().is_exists(chat_id)