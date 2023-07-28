from sqlalchemy import desc
from sqlmodel import Session

from app_database import get_session
from tgbot.models.client_model import ClientDb


class ClientCore:
    def __init__(self, session: Session = next(get_session())):
        self.session = session

    def collect_all_users(self):
        return self.session.query(ClientDb).order_by(desc(ClientDb.client_id))

    def filter_chat_id(self, chat_id: int):
        return ClientDb.chat_id == chat_id