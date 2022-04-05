from os import path
from xmlrpc.client import Boolean
from sqlalchemy import Column, String, Integer, Float, create_engine, ForeignKey, insert
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session


Base = declarative_base()

class JackpotHistory(Base):

    __tablename__ = "JackpotHistory"
    jackpotId = Column('JackpotId', Integer, primary_key=True, nullable=False, autoincrement=True)
    year = Column('Year', Integer, nullable=False)
    round = Column('Round', Integer, nullable=False)
    first = Column('First', Integer, nullable=False)
    second = Column('Second', Integer, nullable=False)
    third = Column('Third', Integer, nullable=False)
    fourth = Column('Fourth', Integer, nullable=False)
    fifth = Column('Fifth', Integer, nullable=False)
    date = Column('Date', String)

    def __repr__(self):
        print_str = f"<JackpotHistory({self.year}年第{self.round}期: {self.first}, {self.second}, {self.third}, {self.fourth}, {self.fifth} 日期:{self.date})>"
        return  print_str

ROOT = path.dirname(path.realpath(__file__))
DBPATH = path.join(ROOT, "daily_cash.db")

class DailyCashContext():

    def __init__(self) -> None:
        self.conn = create_engine(r'sqlite:///'+DBPATH, echo=True)
        self._Session = sessionmaker(bind=self.conn)
        self.session = None

    def open(self) -> Session:
        self.session:Session = self._Session()
        return self.session

    def insert_jackpot(self, jackpot:JackpotHistory) -> bool:
        is_success = False
        try:
            isExisted = self.session.query(JackpotHistory).filter(JackpotHistory.year == jackpot.year).filter(JackpotHistory.round == jackpot.round).all()
            if len(isExisted) <= 0:
                self.session.add(jackpot)
            is_success = True
        except:
            is_success = False
        return is_success

    def commit(self):
        is_success = False
        try:
            self.session.commit()
            is_success = True
        except:
            is_success = False
        return is_success

    def close(self) -> None:
        self.session.close()
        self.conn.dispose()