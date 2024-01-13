import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.getenv("POSTGRES_ASSETS_USER")
password = os.getenv("POSTGRES_ASSETS_PASSWORD")
host = os.getenv("POSTGRES_ASSETS_HOST")
port = os.getenv("POSTGRES_ASSETS_PORT")
database = os.getenv("POSTGRES_ASSETS_DBNAME")

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
Session = sessionmaker(bind=engine)

Base = declarative_base()
