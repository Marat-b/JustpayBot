import uuid
from typing import List, Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from tgbot.models.core_model import CoreModel


class ClientBase(SQLModel):
    CustomerId: str = Field()

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    ClientId: Optional[int]

class ClientRead(ClientBase):
    ClientId: Optional[int]

class Client(ClientBase, CoreModel, table=True):
    __tablename__ = 'client'
    ClientId: Optional[int] = Field(default=None, primary_key=True)
    users: List["User"] = Relationship(back_populates="client")