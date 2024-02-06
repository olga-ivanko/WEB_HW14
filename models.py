from datetime import datetime

from sqlalchemy import String
from db import engine

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class Base(DeclarativeBase):
    pass


class Contact(Base): 
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True,)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(40))
    phone: Mapped[str] = mapped_column(String(20))
    birthday: Mapped[datetime] = mapped_column()
    notes: Mapped[str] = mapped_column(String(250), nullable=True)


if __name__ == "__main__":

    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


