from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, func
from src.database.db import engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), default=1)
    user = relationship("User", backref="contacts")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16))
    email: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

if __name__ == "__main__":

    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
