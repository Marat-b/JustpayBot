import asyncio
import json
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.user_model import UserDb
from tgbot.services.db.user_core import UserCore


class UserDbService(UserCore):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    def __del__(self):
        # Close connection when this object is destroyed
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self._session.close())
            else:
                loop.run_until_complete(self._session.close())
        except Exception:
            pass

    async def create(self, participant_number:int, chat_id:int) -> Optional[UserDb]:
        try:
            if not self._exists(chat_id):
                user = UserDb()
                user.participant_number = participant_number
                user.chat_id = chat_id
                self._session.add(user)
                await self._session.commit()
                await self._session.refresh(user)
                print(f'user={user}')
                return user
            else:
                return None
        except Exception as e:
            print(e)
            await self._session.rollback()
            return None

    async def is_exists(self, chat_id) -> bool:
        result = await self._session.execute(self.collect_all_users()
        .where(self.filter_chat_id(chat_id))
        .where(self.filter_enable(True)
        ))
        user = result.scalars().first()
        return True if user is not None else False

    async def get_by_chat_id(self, chat_id:int):
        result = await self._session.execute(self.collect_all_users().where(self.filter_chat_id(chat_id)))
        user = result.scalars().first()
        return user

    async def get_by_company_id_participant_number(self, company_id:str, participant_number: int):
        result = await self._session.execute(self.collect_all_users()
                                             .where(self.filter_company_id(company_id))
                                             .where(self.filter_number(participant_number)))
        user = result.scalars().first()
        return user

    async def get_by_number(self, participant_number:int) -> UserDb | None:
        """
        Get enabled user by participant number
        :param number:
        :type number:
        :return:
        :rtype:
        """
        result = await self._session.execute(self.collect_all_users()
                                             .where(self.filter_number(participant_number))
                                             .where(self.filter_enable(True)))
        user = result.scalars().first()
        return user

    async def set_enable_status(self, chat_id: int, status: bool) -> None:
        user = await self.get_by_chat_id(chat_id)
        if user is not None:
            user.enable = status
            self._session.add(user)
            await self._session.commit()
            await self._session.refresh(user)


    async def to_str_by_chat_id(self, chat_id:int) -> Optional[str]:
        user = await self.get_by_chat_id(chat_id)
        if user is not None:
            return self._to_str(user)
        else:
            return None

    async def _exists(self, chat_id: int) -> bool:
        count = await self._session.scalar(self.count_all_users().where(self.filter_chat_id(chat_id)))
        return True if count > 0 else False

    def _to_str(self, user) -> str:
        user_dict = user.__dict__
        user_dict.pop('_sa_instance_state', None)
        user_dict.pop('create_date', None)
        user_dict.pop('update_date', None)
        user_dict.pop('user_id', None)
        return json.dumps(user_dict)
