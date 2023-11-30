from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config_data.config import Config, load_config
from .models import Base, User, GameReport


config: Config = load_config()


def add_user(tg_id):
    engine = create_engine(config.db.db_address, echo=True)  # создаем фабрику для соединения с базой данных
    Base.metadata.create_all(engine)                         # создаем таблицы, если они не созданы
    Session = sessionmaker(bind=engine)                      # создаем соединение с бд
    session = Session()                                      # записываем в переменную
    user = session.query(User).filter(User.user_id == tg_id).first()
    if user is None:
        new_user = User(user_id=tg_id)
        session.add(new_user)
        session.commit()


def create_game_report(tg_id: int, game: int, win: bool, defeats: bool, attempts: int):
    engine = create_engine(config.db.db_address, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.user_id == tg_id).first()
    new_game = GameReport(game_number=game, win=win, defeat=defeats, attempts=attempts, owner=user.id)
    session.add(new_game)
    session.commit()


def count_games(tg_id):
    engine = create_engine(config.db.db_address, echo=True)  # создаем фабрику для соединения с базой данных
    Base.metadata.create_all(engine)  # создаем таблицы, если они не созданы
    Session = sessionmaker(bind=engine)  # создаем соединение с бд
    session = Session()
    user = session.query(User).filter(User.user_id == tg_id).first()
    game_number = session.query(GameReport).filter(GameReport.owner == user.id).count()
    session.commit()
    return game_number
