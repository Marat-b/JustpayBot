from app_database import get_session
from tgbot.models.client_model import ClientDb


class ClientDbService:
    def __init__(self, session=next(get_session())):
        self.session = session

    def create(self, company_id:str, customer_id:str, chat_id:int) -> ClientDb:
        client = ClientDb(company_id=company_id, customer_id=customer_id, chat_id=chat_id)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

