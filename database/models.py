from datetime import datetime


from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    # create class User with Column connection_date - date, when user started bot, user_id - telegram id
    # User has connection to reports
    
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    reports = relationship('GameReport', backref='report', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.user_id


class GameReport(Base):
    # GameReport - report about finished game, with column owner - user, who played, 
    # game_number - number of game, win, defeat and attempts - number of attempts,
    # for which the result (win or defeat) was achieved 
    # if win = True and defeat = True in same game, that means draw

    __tablename__ = 'GameReports'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('Users.id'), nullable=False)
    game_number = Column(Integer, nullable=False)
    win = Column(Boolean)
    defeat = Column(Boolean)
    attempts = Column(Integer, nullable=False)

    def __repr__(self):
        return self.game_number
