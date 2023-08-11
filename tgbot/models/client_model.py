from typing import List, Optional

from sqlalchemy import Boolean, Column, Integer, String

from tgbot.models.core_model import CoreModel
from tgbot.models.get_base import Base

class ClientDb(CoreModel, Base):
    __tablename__ = 'client'
    client_id: Optional[int] = Column(Integer, primary_key=True)
    chat_id: Optional[int] = Column(Integer) # Field(description='chat id from bot')
    customer_id: str = Column(String) #Field(description='customer id from JustPay')
    customer_number: int = Column(Integer, default=0) # Field(description='customer number from JustPay', default=0)
    enable: bool = Column(Boolean, default=True) # Field(default=True)
    # users: List["UserDb"] = Relationship(back_populates="client")