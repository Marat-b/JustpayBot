from typing import Optional

from app_database import get_session
from tgbot.models.user_model import UserDb


class UserDbService:
    def __init__(self, session=next(get_session())):
        self._session = session

    def create(self, company_id:str, participant_number:int, chat_id:int) -> Optional[UserDb]:
        try:
            user = UserDb(company_id=company_id,participant_number=participant_number, chat_id=chat_id)
            self._session.add(user)
            self._session.commit()
            self._session.refresh(user)
            print(f'user={user}')
            return user
        except Exception as e:
            # psycopg2.errors.UniqueViolation
            print(e)
            return None
