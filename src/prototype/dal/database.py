import sqlite3
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
db = sqlite3.connect('../dal/event.db', timeout=50)
Base = declarative_base()
DB_URL = "sqlite:///../dal/event.db"
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
session = SessionLocal()


def create_user():
    db.execute("""CREATE TABLE IF NOT EXISTS user(
       userid INT UNIQUE NOT NULL PRIMARY KEY,
       usernic TEXT NOT NULL,
       userfname TEXT NOT NULL,
       userrole TEXT NOT NULL, 
       userplace TEXT NOT NULL);
""")
    db.commit()


def create_event():
    db.execute("""CREATE TABLE IF NOT EXISTS event(
       eventid INT UNIQUE PRIMARY KEY,
       promocode STRING NOT NULL,
       eventtype STRING NOT NULL,
       eventname STRING NOT NULL,
       eventdescription TEXT NOT NULL,
       eventstart TEXT NOT NULL,
       eventend TEXT NOT NULL,
       eventmanedger STRING NOT NULL
       );
""")
    db.commit()


def create_ver():
    db.execute("""CREATE TABLE IF NOT EXISTS verification(
       verid INT NOT NULL PRIMARY KEY,
       userid INT NOT NULL REFERENCES user,
       eventid INT NOT NULL REFERENCES event,
       verstatus INT NOT NULL);
""")
    db.commit()


class User(Base):
    __tablename__ = "user"
    userid = Column(Integer, primary_key=True, unique=True)
    usernic = Column(String)
    userfname = Column(String)
    userrole = Column(Integer)
    userplace = Column(String)

    def update_user(self):
        session.add(self)
        session.commit()

    def delete_user(self):
        session.delete(self)
        session.commit()


class Event(Base):
    __tablename__ = "event"
    eventid = Column(Integer, primary_key=True)
    promocode = Column(String)
    eventtype = Column(String)
    eventname = Column(String)
    eventdescription = Column(String)
    eventstart = Column(String)
    eventend = Column(String)
    eventmanedger = Column(String)

    def update_event(self):
        session.add(self)
        session.commit()

    def delete_event(self):
        session.delete(self)
        session.commit()


class Ver(Base):
    __tablename__ = "verification"
    verid = Column(Integer, primary_key=True)
    userid = Column(String, ForeignKey('user.usernic'))
    eventid = Column(Integer, ForeignKey('event.eventid'))
    verstatus = Column(Integer)

    def update_ver(self):
        session.add(self)
        session.commit()

    def delete_ver(self):
        session.delete(self)
        session.commit()


Base.metadata.create_all(engine)


def get_status(n, m):
    q = SessionLocal().query(Ver).filter(Ver.userid == n, Ver.eventid == m)
    for i in q:
        return i.verstatus


def get_verevent():
    q = SessionLocal().query(Ver)
    for i in q:
        return i.eventid


def get_userinfo():
    q = SessionLocal().query(User)
    for i in q:
        return [i.userid, i.usernic, i.userfname, i.userrole, i.userplace]


def get_eventinfo():
    q = SessionLocal().query(Event)
    for i in q:
        return [i.eventid, i.promocode, i.eventtype, i.eventname, i.eventdescription, i.eventstart, i.eventend,
                i.eventmanedger]


def add_user(info):
    session.add(User(userid=info[0], usernic=info[1], userfname=info[2], userrole=info[3], userplace=info[4]))
    session.commit()
    if get_user(info[0]):
        return 0
    else:
        return 1


def get_event(n):
    return session.query(Event).filter(Event.eventid == n).first()


def get_user(n):
    return session.query(User).filter(User.userid == n).first()


def get_ver(n, m):
    return session.query(Ver).filter(Ver.userid == n, Ver.eventid == m).first()


def add_ver(n, m):
    session.add(Ver(userid=n, eventid=m, verstatus=0))
    session.commit()


def update_verevent(n, m):
    SessionLocal().query(Ver).filter(Ver.userid == n).update({'eventid': "new"})
    SessionLocal().commit()
    if get_verevent() == m:
        return 0
    else:
        return 1


def update_verstatus(n, m):
    SessionLocal().query(Ver).filter(Ver.userid == n, Ver.eventid == m).update({'verstatus': Ver.verstatus + 1})
    SessionLocal().commit()


def get_events():
    return session.query(Event).all()


def get_event_by_id(event_id):
    return session.query(Event).get(event_id)


def get_users():
    return session.query(User).all()


def get_user_by_id(user_id):
    return session.query(User).get(user_id)


def get_user_by_nick(user_nick):
    return session.query(User).filter(User.usernic == user_nick).first()


def get_checkin_users(event_id):
    users = []
    ver = session.query(Ver).filter(Ver.eventid == event_id).all()
    for v in ver:
        users.append(get_user_by_id(v.userid))
    return users
