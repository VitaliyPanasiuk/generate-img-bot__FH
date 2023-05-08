from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    db_uri: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token="5257942822:AAFqBBqGZs6UJZsF3fJ6fY-f8pCFQelxXRw",
            admin_ids=[762342298],
            use_redis=False,
        ),
        db=DbConfig(
            host='localhost',
            password='2545',
            user='postgres',
            database='gen-img',
            db_uri='DB_URI'
        ),
        misc=Miscellaneous()
    )

# insert into tn_tariff (name, costs) values ('donate-visa',30),('donate-visa direct',30),('donate-card transaction',30),('tn - tn',30),('tn - bank',30),('wn to tn',30),('wn to bank pdf',30),('tn - tn pdf ',30);