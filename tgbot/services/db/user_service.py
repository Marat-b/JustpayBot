import json
from typing import Optional

from sqlmodel import Session

from app_database import get_session
from tgbot.models.user_model import UserDb
from tgbot.services.db.user_core import UserCore


class UserDbService(UserCore):
    def __init__(self, session:Session=next(get_session())):
        super().__init__(session)
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
            self._session.rollback()
            return None

    def get_by_chat_id(self, chat_id:int):
        user = self.collect_all_users().filter(self.filter_chat_id(chat_id)).first()
        return user

    def get_by_company_id_participant_number(self, company_id:str, participant_number: int):
        user = self.collect_all_users().filter(self.filter_company_id(company_id)).\
            filter(self.filter_number(participant_number)).first()
        return user

    def get_by_number(self, number:int):
        user = self.collect_all_users().filter(self.filter_number(number)).first()
        return user


    def to_str_by_chat_id(self, chat_id:int) -> Optional[str]:
        user = self.get_by_chat_id(chat_id)
        if user is not None:
            return self._to_str(user)
        else:
            return None
    def _to_str(self, user) -> str:
        user_dict = user.__dict__
        user_dict.pop('_sa_instance_state', None)
        user_dict.pop('create_date', None)
        user_dict.pop('update_date', None)
        user_dict.pop('user_id', None)
        return json.dumps(user_dict)
