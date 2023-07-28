from typing import Optional

from marshmallow.fields import Bool

from app_database import get_session
from tgbot.models.client_model import ClientDb
from tgbot.services.db.client_core import ClientCore


class ClientDbService(ClientCore):
    def __init__(self, session=next(get_session())):
        super().__init__(session)
        self._session = session

    def create(self, customer_id:str, customer_number:int, chat_id:int) -> Optional[ClientDb]:
        if not self._exists(chat_id):
            client = ClientDb(customer_id=customer_id, customer_number=customer_number, chat_id=chat_id)
            self._session.add(client)
            self._session.commit()
            self._session.refresh(client)
            return client
        else:
            return None

    def _exists(self, chat_id: int) -> bool:
        count = self.collect_all_users().filter(self.filter_chat_id(chat_id)).count()
        return True if count > 0 else False

