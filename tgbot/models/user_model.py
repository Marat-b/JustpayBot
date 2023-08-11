from typing import Optional

from sqlalchemy import Boolean, Column, Integer, String

from sqlalchemy import UniqueConstraint
from tgbot.models.core_model import CoreModel
from tgbot.models.get_base import Base


# Base=declarative_base()
class UserDb(CoreModel, Base):
    __tablename__ = 'user'
    # client_id: Optional[int] = (default=None, foreign_key="client.client_id
    chat_id: int = Column(Integer) #
    company_id: Optional[str] = Column(String) #
    enable: bool = Column(Boolean, default=True)
    participant_number: int = Column(Integer)
    user_id: Optional[int] = Column(Integer,  primary_key=True)
    __table_args__ = (UniqueConstraint('chat_id', 'company_id','participant_number',
                                      name='_chat_company_participant'),)
    # client: Optional[ClientDb] = Relationship(back_populates="users")



# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
#
# engine = create_engine(sqlite_url, echo=True)
#
#
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# if __name__ == "__main__":
    # create_db_and_tables()
    # with Session(engine) as session:
    #     customer = ClientDb(CustomerId='customer_id', ChatId=0)
    #     # customer2 = ClientDb(customerId='customer_id2')
    #     print(f'customer={customer}')
    #     user = User(ParticipantId='participant_id',ChatId=1,  client=customer )
    #     session.add(user)
    #     session.commit()
    #     session.refresh(user)
    #     user2 = User(ParticipantId='participant_id2', ChatId=2, client=customer)
    #     session.add(user2)
    #     session.commit()
    #     session.refresh(user2)
    #     user3 = User(ParticipantId='participant_id3', ChatId=3)
    #     session.add(user3)
    #     session.commit()
    #     session.refresh(user3)
    #     print(f'user={user3}')
    #     print(f'customer={customer}')
    #     user3.client = customer
    #     session.add(user3)
    #     session.commit()
    #     session.refresh(user3)
