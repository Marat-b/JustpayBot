import uuid
from typing import List, Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

# from tgbot.models.UserModel import UserInDb


class ClientBase(SQLModel):
    CustomerId: str = Field()

class Client(ClientBase, table=True):
    ClientId: Optional[int] = Field(default=None, primary_key=True)
    users: List["User"] = Relationship(back_populates="client")