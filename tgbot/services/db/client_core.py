from sqlalchemy import Integer, cast, desc
from sqlalchemy.orm import Session

# from sqlmodel import Session

from app_database import get_session
from tgbot.models.client_model import ClientDb


class ClientCore:
    def __init__(self, session: Session = next(get_session())):
        self.session = session

    def collect_all_customers(self):
        return self.session.query(ClientDb).order_by(desc(cast(ClientDb.client_id,Integer)))

    def filter_enable(self,enable: bool):
        return ClientDb.enable == enable
    def filter_chat_id(self, chat_id: int):
        return ClientDb.chat_id == chat_id

    def filter_customer_id(self, customer_id: str):
        return ClientDb.customer_id == customer_id