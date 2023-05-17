
from pydantic import BaseSettings

from tgbot import config


class Settings(BaseSettings):
    # server_host: str = config.WEB_SERVER_HOST
    # server_port: int = config.WEB_SERVER_PORT

    # database_url: str = r"sqlite:///C:\Softz\Projects\LoyaltyProjects\db_api\test.db"
    # database_url: str = r"sqlite:///C:\Softz\Projects\LoyaltyProjects\db_api\database.db"
    database_url = config.POSTGRES_URI

    jwt_secret: str = 's'
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600


settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8',

)

if __name__ == '__main__':
    print(settings)
