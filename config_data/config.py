from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str            # Token to access telegram-bot


@dataclass
class DB:
    db_address: str       # Database address


@dataclass
class Config:
    tg_bot: TgBot
    db: DB


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), db=DB(db_address=env('DB_ADDRESS')))
