from sqlalchemy import Column, Integer, String, ForeignKey, Table, Time
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
db_url = "sqlite:///../dal/school21.db"
school21_engine = create_engine(db_url, pool_pre_ping=True)
school21_SessionLocal = sessionmaker(autoflush=False, bind=school21_engine)


class Users(Base):
    __tablename__ = "users"
    usernic = Column(String, primary_key=True, unique=True)
    userrole = Column(Integer)


def check_user(n):
    if school21_SessionLocal().query(Users).filter(Users.usernic == n).all():
        return 0
    else:
        return 1


def get_role(n):
    role = school21_SessionLocal().query(Users).filter(Users.usernic == n).all()[0]
    return role.userrole
