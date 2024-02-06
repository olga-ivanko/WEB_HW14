from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import configparser
import pathlib


file_config = pathlib.Path(__file__).parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DB", "USER")
password = config.get("DB", "PASSWORD")
db_name = config.get("DB", "DATABASE")
domain = config.get("DB", "DOMAIN")

url = f"postgresql://{username}:{password}@{domain}:5432/{db_name}"
engine = create_engine(url, echo=False)

DBSession = sessionmaker(bind=engine)
session = DBSession()
