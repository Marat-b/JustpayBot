from typing import List, Optional

from marshmallow.fields import Bool

from app_database import get_session

from tgbot.models.client_model import ClientDb
from tgbot.services.db.client_core import ClientCore


class ClientDbService(ClientCore):
    def __init__(self, session=next(get_session())):
        super().__init__(session)
        self._session = session

    def create(self, customer_id:str, customer_number:int, chat_id:int) -> Optional[ClientDb]:
        if not self._exists(chat_id, customer_id):
            client = ClientDb(customer_id=customer_id, customer_number=customer_number, chat_id=chat_id)
            self._session.add(client)
            self._session.commit()
            self._session.refresh(client)
            return client
        else:
            return None

    def is_exists(self, chat_id) -> bool:
        customer = (self.collect_all_customers()
                    .filter(self.filter_chat_id(chat_id))
                    # .filter(self.filter_customer_id(customer_id))
                    .filter(self.filter_enable(
            True)).first())
        return True if customer is not None else False

    def get_all_active_clients(self) -> List[ClientDb]:
        return self.collect_all_customers().filter(self.filter_enable(True)).all()

    def get_by_chat_id(self, chat_id: int) -> ClientDb:
        customer = self.collect_all_customers().filter(self.filter_chat_id(chat_id)).first()
        return  customer

    def get_chat_id_by_customer_id(self, customer_id) -> List[ClientDb]:
        """
        Get list of Chat Id by Customer Id
        :param customer_id:
        :type customer_id:
        :return:
        :rtype:
        """
        customers = self.collect_all_customers()\
            .filter(self.filter_customer_id(customer_id))\
            .filter(self.filter_enable(True))\
            .all()
        # if customer is not None:
        #     print(f'get_chat_id_by_customer_id chat_id={customer.chat_id}')
        # else:
        #     print('get_chat_id_by_customer_id customer is None')
        customer_chat_ids = [customer.chat_id for customer in customers]
        return customer_chat_ids

    def set_enable_status(self, chat_id: int, status: bool) -> None:
        customer = self.get_by_chat_id(chat_id)
        if customer is not None:
            customer.enable = status
            self._session.add(customer)
            self._session.commit()
            self._session.refresh(customer)

    def _exists(self, chat_id: int, customer_id: str) -> bool:
        count = (self.collect_all_customers()
                 .filter(self.filter_chat_id(chat_id))
                .filter(self.filter_customer_id(customer_id))
                 .count())
        return True if count > 0 else False

