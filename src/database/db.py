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

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{username}:{password}@{domain}:5432/{db_name}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

DBSession = sessionmaker(autocommit = False, autoflush = False, bind=engine)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
