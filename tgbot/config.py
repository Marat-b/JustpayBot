from dataclasses import dataclass
from typing import Optional

from environs import Env
from sqlalchemy import URL


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    def uri(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.database}"

    # For SQLAlchemy
    def construct_sqlalchemy_url(self) -> URL:
        # if not host:
        #     host = self.host
        # if not port:
        #     port = self.port
        return URL.create(
            drivername=f"postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        # return uri.render_as_string(hide_password=False)


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class RedisConfig:
    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]
    redis_user: Optional[str]
    redis_hash_name: Optional[str]

    def dsn(self) -> str:
        if self.redis_pass:
            return f"redis://{self.redis_user}:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

@dataclass
class RabbitConfig:
    rabbit_pass: Optional[str]
    rabbit_user: Optional[str]
    rabbit_host: Optional[str]
    rabbit_port: Optional[str]
    def dsn(self) -> str:
        return f"amqp://{self.rabbit_user}:{self.rabbit_pass}@{self.rabbit_host}:{self.rabbit_port}/"

@dataclass
class Miscellaneous:
    other_params: str = None

@dataclass
class SQLiteConfig:
    db_path: str

@dataclass
class MailConfig:
    smtp_server: str
    from_addr: str
    to_addr: str
    # subject: str
    # body_text: str
    mail_user: str
    mail_password: str

@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous
    db: DbConfig = None
    redis: RedisConfig = None
    sqlite: SQLiteConfig =None
    rabbit: RabbitConfig = None
    mail: MailConfig = None


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS")
        ),

        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('POSTGRES_PASSWORD'),
            user=env.str('POSTGRES_USER'),
            database=env.str('POSTGRES_DB'),
        ),

        rabbit=RabbitConfig(
            rabbit_host=env.str("RABBITMQ_HOST"),
            rabbit_user= env.str("RABBITMQ_USER"),
            rabbit_pass=env.str("RABBITMQ_PASSWORD"),
            rabbit_port=env.str("RABBITMQ_PORT")
        ),

        mail=MailConfig(smtp_server=env.str("SMTP_SERVER"),
                        from_addr=env.str("FROM_ADDR"),
                        to_addr=env.str("TO_ADDR"),
                        # subject=env.str("SUBJECT"),
                        # body_text=env.str("BODY_TEXT"),
                        mail_user=env.str("MAIL_USER"),
                        mail_password=env.str("MAIL_PASSWORD")
                        ),

        redis=RedisConfig(
            redis_pass=env.str("REDIS_PASSWORD"),
            redis_port=env.int("REDIS_PORT"),
            redis_host=env.str("REDIS_HOST"),
            redis_user=env.str("REDIS_USER"),
            redis_hash_name=env.str("REDIS_HASH_NAME")
        ),

        # sqlite = SQLiteConfig(db_path=env.str("SQLITE_DB"),),

        misc=Miscellaneous()
    )
