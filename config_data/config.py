from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class DB:
    db_address: str       # Адресс для доступа к базе данных


@dataclass
class Config:
    tg_bot: TgBot
    db: DB


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), db=DB(db_address=env('DB_ADDRESS')))
