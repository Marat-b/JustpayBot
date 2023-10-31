from sqlalchemy import Column, DateTime, func

class CoreModel():
    create_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    update_date = Column(DateTime(timezone=True), nullable=False, server_onupdate=func.now(), server_default=func.now())
