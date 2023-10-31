from sqlalchemy import Integer, cast, desc, func, select
from tgbot.models.client_model import ClientDb


class ClientCore:
    # def __init__(self, session: AsyncSession=get_session):
    #     self.session = session

    def collect_all_customers(self):
        return select(ClientDb).order_by(desc(cast(ClientDb.client_id,Integer)))

    def collect_all_customers_by_client_id(self):
        return select(ClientDb.client_id).order_by(desc(cast(ClientDb.client_id,Integer)))

    def count_all_customers(self):
        return select(func.count(ClientDb.client_id))

    def filter_enable(self,enable: bool):
        return ClientDb.enable == enable
    def filter_chat_id(self, chat_id: int):
        return ClientDb.chat_id == chat_id

    def filter_customer_id(self, customer_id: str):
        return ClientDb.customer_id == customer_id