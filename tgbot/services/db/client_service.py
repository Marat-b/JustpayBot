from tgbot.models.customer_model import Client


class ClientService:
    def __init__(self, session):
        self.session = session

    def create(self, customer_id:str):
        client = Client(CustomerId=customer_id)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client