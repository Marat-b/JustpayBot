import uuid
from typing import List, Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from tgbot.models.core_model import CoreModel


# class ClientBase(SQLModel):
#     CustomerId: str = Field()
#     ChatId: Optional[int]
#
# class ClientCreate(ClientBase):
#     pass
#
# class ClientUpdate(ClientBase):
#     ClientId: Optional[int]
#
# class ClientRead(ClientBase):
#     ClientId: Optional[int]

class ClientDb(CoreModel, table=True):
    __tablename__ = 'client'
    client_id: Optional[int] = Field(default=None, primary_key=True, description='Identity')
    chat_id: Optional[int] = Field(description='chat id from bot')
    company_id: str = Field(description='company id from JustPay')
    customer_number: int = Field(description='customer number from JustPay')
    enable: bool = Field(default=True)
    # users: List["UserDb"] = Relationship(back_populates="client")