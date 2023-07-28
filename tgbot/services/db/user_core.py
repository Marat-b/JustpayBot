from sqlalchemy import desc
from sqlmodel import Session

from app_database import get_session
from tgbot.models.user_model import UserDb


class UserCore:
    def __init__(self, session: Session = next(get_session())):
        self.session = session

    def collect_all_users(self):
        return self.session.query(UserDb).order_by(desc(UserDb.user_id))

    def filter_enable(self, enable: bool):
        return UserDb.enable == enable

    def filter_chat_id(self, chat_id: int):
        return UserDb.chat_id == chat_id

    def filter_company_id(self, company_id: str):
        return UserDb.company_id == company_id

    def filter_number(self, number: int):
        return UserDb.participant_number == number