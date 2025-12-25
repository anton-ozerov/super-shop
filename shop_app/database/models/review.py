from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from shop_app.database.database import Base


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    parameter_id: Mapped[int]
    start: Mapped[int] = mapped_column(SmallInteger)
    comment: Mapped[str | None]

# Что делать с параметром и валидация звезд от 1 до 5
