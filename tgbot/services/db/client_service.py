from app_database import get_session
from tgbot.models.client_model import ClientDb


class ClientDbService:
    def __init__(self, session=next(get_session())):
        self._session = session

    def create(self, company_id:str, customer_number:int, chat_id:int) -> ClientDb:
        client = ClientDb(company_id=company_id, customer_number=customer_number, chat_id=chat_id)
        self._session.add(client)
        self._session.commit()
        self._session.refresh(client)
        return client

