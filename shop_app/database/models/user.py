from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

import uuid
from shop_app.database.database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(default='Anonymous', nullable=False)
    email: Mapped[str | None] = mapped_column(nullable=True)
    phone: Mapped[str | None] = mapped_column(nullable=True)
    is_blocked: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)

    reviews: Mapped[list['Review']] = relationship(
        back_populates='review',
    )
    orders: Mapped[list['Order']] = relationship(
        back_populates='order',
    )
    promocodes: Mapped[list['Promocode']] = relationship(
        back_populates='promocode',
        secondary='user_promocode_assignment',
    )
