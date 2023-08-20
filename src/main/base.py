from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Verbindungsaufbau wird nach folgender Beschreibung aus der SQLalchemy-Dokumentation ausgeführt:
# https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
url_object = URL.create(
    "postgresql",
    username="postgres",
    password="@Postgres123",
    host="localhost",
    database="personalstammdaten",
)

engine = create_engine(url_object)

# https://docs.sqlalchemy.org/en/20/orm/session_basics.html
Session = sessionmaker(bind=engine)

Base = declarative_base()