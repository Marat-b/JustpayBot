from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class CoreModel(SQLModel):
    CreateDate: datetime = Field(default=None,
                                          sa_column=Column(DateTime(timezone=True), nullable=False, default=func.now()),
                                          description='Create at', alias='createDate')
    UpdateDate: datetime = Field(default=None,
                                          sa_column=Column(DateTime(timezone=True), nullable=False, default=func.now()),
                                          description='Update at', alias='updateDate'
                                          )