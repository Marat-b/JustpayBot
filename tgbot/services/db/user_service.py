from app_database import get_session
from tgbot.models.user_model import UserDb


class UserDbService:
    def __init__(self, session=next(get_session())):
        self.session = session

    def create(self, company_id:str, participant_number:int, chat_id:int) -> UserDb:
        user = UserDb(company_id=company_id,participant_number=participant_number, chat_id=chat_id)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
