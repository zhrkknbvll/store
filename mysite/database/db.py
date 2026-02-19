from sqlalchemy.engine import create_engine# база данныхка улап койот
from sqlalchemy.orm import sessionmaker#сессияны апйда кылуу
from sqlalchemy.ext.declarative import declarative_base#

DB_URL = 'postgresql://postgres:admin@localhost/shop_fastapi'
engine = create_engine(DB_URL) #базага путь

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base() #моделканы тузгонго жардам берет


