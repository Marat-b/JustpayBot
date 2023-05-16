import uuid
from typing import Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine

from tgbot.models.core_model import CoreModel
from tgbot.models.customer_model import Client


class UserBase(SQLModel):
    ParticipantId: str = Field(description='participants')

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    UserId: Optional[int]

class UserRead(UserBase):
    UserId: Optional[int]
    ClientId: Optional[int]

class User(UserBase, CoreModel, table=True):
    UserId: Optional[int] = Field(default=None, primary_key=True)
    ClientId: Optional[int] = Field(default=None, foreign_key="client.ClientId")
    client: Optional[Client] = Relationship(back_populates="users")

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    with Session(engine) as session:
        customer = Client(CustomerId='customer_id')
        # customer2 = Client(customerId='customer_id2')
        print(f'customer={customer}')
        user = User(ParticipantId='participant_id', client=customer )
        session.add(user)
        session.commit()
        session.refresh(user)
        user2 = User(ParticipantId='participant_id2', client=customer)
        session.add(user2)
        session.commit()
        session.refresh(user2)
        user3 = User(ParticipantId='participant_id3')
        session.add(user3)
        session.commit()
        session.refresh(user3)
        print(f'user={user3}')
        print(f'customer={customer}')
        user3.client = customer
        session.add(user3)
        session.commit()
        session.refresh(user3)
