from typing import Optional

from sqlmodel import Field, Relationship

# from tgbot.models.app_database import create_db_and_tables
from tgbot.models.core_model import CoreModel
from tgbot.models.client_model import ClientDb


# class UserBase(SQLModel):
#     ParticipantId: str = Field(description='participants')
#     ChatId:int
#
#
# class UserCreate(UserBase):
#     pass
#
# class UserUpdate(UserBase):
#     UserId: Optional[int]
#
# class UserRead(UserBase):
#     UserId: Optional[int]
#     ClientDbId: Optional[int]

class UserDb(CoreModel, table=True):
    __tablename__ = 'user'
    # client_id: Optional[int] = Field(default=None, foreign_key="client.client_id")
    chat_id: int = Field(description='chat id from bot')
    company_id: str = Field(description='company id from JustPay')
    enable: bool = Field(default=True)
    participant_id: str = Field(description='participant id from Loyalty')
    user_id: Optional[int] = Field(default=None, primary_key=True)
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
