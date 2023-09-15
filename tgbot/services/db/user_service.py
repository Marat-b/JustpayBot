import json
from typing import Optional

from sqlalchemy.orm import Session

# from sqlmodel import Session

from app_database import get_session
from tgbot.models.user_model import UserDb
from tgbot.services.db.user_core import UserCore


class UserDbService(UserCore):
    def __init__(self, session:Session=next(get_session())):
        super().__init__(session)
        self._session = session

    def create(self, participant_number:int, chat_id:int) -> Optional[UserDb]:
        try:
            if not self._exists(chat_id):
                user = UserDb(participant_number=participant_number, chat_id=chat_id)
                self._session.add(user)
                self._session.commit()
                self._session.refresh(user)
                print(f'user={user}')
                return user
            else:
                return None
        except Exception as e:
            # psycopg2.errors.UniqueViolation
            print(e)
            self._session.rollback()
            return None

    def is_exists(self, chat_id) -> bool:
        user = self.collect_all_users().filter(self.filter_chat_id(chat_id)).filter(
            self.filter_enable(
                True
            )
        ).first()
        return True if user is not None else False

    def get_by_chat_id(self, chat_id:int):
        user = self.collect_all_users().filter(self.filter_chat_id(chat_id)).first()
        return user

    def get_by_company_id_participant_number(self, company_id:str, participant_number: int):
        user = self.collect_all_users().filter(self.filter_company_id(company_id)).\
            filter(self.filter_number(participant_number)).first()
        return user

    def get_by_number(self, participant_number:int) -> UserDb | None:
        """
        Get enabled user by participant number
        :param number:
        :type number:
        :return:
        :rtype:
        """
        user = self.collect_all_users().filter(self.filter_number(participant_number)).filter(self.filter_enable(
            True)).first()
        return user

    def set_enable_status(self, chat_id: int, status: bool) -> None:
        user = self.get_by_chat_id(chat_id)
        if user is not None:
            user.enable = status
            self._session.add(user)
            self._session.commit()
            self._session.refresh(user)


    def to_str_by_chat_id(self, chat_id:int) -> Optional[str]:
        user = self.get_by_chat_id(chat_id)
        if user is not None:
            return self._to_str(user)
        else:
            return None

    def _exists(self, chat_id: int) -> bool:
        count = self.collect_all_users().filter(self.filter_chat_id(chat_id)).count()
        return True if count > 0 else False

    def _to_str(self, user) -> str:
        user_dict = user.__dict__
        user_dict.pop('_sa_instance_state', None)
        user_dict.pop('create_date', None)
        user_dict.pop('update_date', None)
        user_dict.pop('user_id', None)
        return json.dumps(user_dict)
