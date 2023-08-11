from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tgbot.config import load_config
from tgbot.models.client_model import Base

config = load_config(".env")

engine = create_engine(
    config.db.uri(),
)

def create_db_and_tables():
    Base.metadata.create_all(engine)

# def create_jbot(engin):
#     SQLModel.metadata.create_all(engin)
#     pass

def get_session():
    with Session(engine) as session:
        yield session

