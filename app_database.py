
from sqlmodel import create_engine, Session, SQLModel
from tgbot.models.client_model import ClientDb
from tgbot.models.user_model import UserDb

from tgbot.config import load_config

config = load_config(".env")

engine = create_engine(
    config.db.uri(),
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    pass

def create_jbot(engin):
    SQLModel.metadata.create_all(engin)
    pass

def get_session():
    with Session(engine) as session:
        yield session
