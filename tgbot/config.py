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
            token="5890500081:AAGqjwyJJ7ZOL-KdvtDIi6ieuL1DbHnrOT4",
            admin_ids=[762342298,6197913672],
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
