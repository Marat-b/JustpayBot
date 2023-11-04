import asyncio
from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.infrastructure.database.functions.setup import get_session
from tgbot.models.client_model import ClientDb
from tgbot.services.db.client_core import ClientCore


class ClientDbService(ClientCore):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session
        # self._session_pool = get_session()

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

    async def create(self, customer_id: str, customer_number: int, chat_id: int) -> Optional[ClientDb]:
        # async with self._session_pool() as session:
        is_exists = await self._exists(chat_id, customer_id)
        if not is_exists:
            # client = ClientDb(customer_id=customer_id, customer_number=customer_number, chat_id=chat_id)
            client = ClientDb()
            client.customer_id = customer_id
            client.customer_number = customer_number
            client.chat_id = chat_id
            self._session.add(client)
            await self._session.commit()
            await self._session.refresh(client)
            return client
        else:
            return None

    async def is_exists(self, chat_id) -> bool:
        # async with self._session_pool() as session:
        result = await self._session.execute(
            self.collect_all_customers()
            .where(self.filter_chat_id(chat_id))
            .where(self.filter_enable(True))
            )
        customer = result.scalars().first()
        return True if customer is not None else False

    async def get_all_active_clients(self) -> List[ClientDb]:
        # async with self._session_pool() as session:
        result = await self._session.execute(self.collect_all_customers().where(self.filter_enable(True)))
        customer = result.scalars().all()
        return customer

    async def get_by_chat_id(self, chat_id: int) -> List[ClientDb]:
        # async with self._session_pool() as session:
        result = await self._session.execute(self.collect_all_customers().where(self.filter_chat_id(chat_id)))
        customers = result.scalars().all()
        return customers

    async def get_chat_id_by_customer_id(self, customer_id) -> List[int]:
        """
        Get list of Chat Id by Customer Id
        :param customer_id:
        :type customer_id:
        :return:
        :rtype:
        """
        # async with self._session_pool() as session:
        result = await self._session.execute(
            self.collect_all_customers() \
            .where(self.filter_customer_id(customer_id)) \
            .where(self.filter_enable(True))
            )
        customers = result.scalars().all()
        customer_chat_ids = [customer.chat_id for customer in customers]
        return customer_chat_ids

    async def set_enable_status(self, chat_id: int, status: bool) -> list[ClientDb]:
        # async with self._session_pool() as session:
        customers = await self.get_by_chat_id(chat_id)
        for customer in customers:
            customer.enable = status
            customer.update_date = datetime.now()
            self._session.add(customer)
            await self._session.commit()
            await self._session.refresh(customer)
        return customers

    async def _exists(self, chat_id: int, customer_id: str) -> bool:
        # async with self._session_pool() as session:
        print(f'chat_id={chat_id}, customer_id={customer_id}')
        count = await self._session.scalar(
           self.count_all_customers()
            .where(self.filter_chat_id(chat_id))
            .where(self.filter_customer_id(customer_id))
            )
        print(f'_exists count={count}')
        return True if count > 0 else False
