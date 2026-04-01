from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import TIMESTAMP


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'


    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    is_permission: Mapped[bool] = mapped_column(default=False)
    stars: Mapped[int] = mapped_column(default=0)


class Persons(Base):
    __tablename__ = 'persons'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone: Mapped[str]
    address: Mapped[str]
    iin: Mapped[str]
    email: Mapped[str]
    image: Mapped[str] = mapped_column(String(256))






