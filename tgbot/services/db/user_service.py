from app_database import get_session
from tgbot.models.client_model import ClientDb
from tgbot.models.user_model import UserDb


class UserDbService:
    def __init__(self, session=next(get_session())):
        self.session = session

    def create(self, company_id:str, participant_id:str, chat_id:int) -> UserDb:
        # if client is None:
        user = UserDb(company_id=company_id,participant_id=participant_id, chat_id=chat_id)
        # else:
        #     user = UserDb(participant_id=participant_id, chat_id=chat_id, client=client)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
