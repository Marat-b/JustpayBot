from tgbot.services.db.client_service import ClientDbService


def set_client_enable_status(chat_id, status)->None:
    client_service = ClientDbService()
    client_service.set_enable_status(chat_id, status)