from sqlalchemy import SmallInteger, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID, ENUM

import datetime, uuid
from typing import Any
from shop_app.database.database import Base
from shop_app.enums import DiscountType


class Promocode(Base):
    __tablename__ = 'promocode'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    value: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    active_until_date: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    is_combined_w_other_promotions: Mapped[bool] = mapped_column(default=False, nullable=False)
    how_many_times_per_user: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    discount_type: Mapped[DiscountType] = mapped_column(
        ENUM(
            DiscountType,
            name='discount_type_enum',
            check_constraint=True,
        ),
        nullable=False,
    )
    included_products_ids: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True)
    excluded_products_ids: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True)

    users: Mapped['User'] = relationship(
        back_populates='user',
        secondary='user_promocode_assignment',
    )


class UserPromocodeAssignment(Base):
    __tablename__ = "user_promocode_assignment"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'user.id',
            name='user_promocode_assignment_user_id_foreign_key',
            ondelete='CASCADE',
        ),
    )
    promocode_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'user.id',
            name='user_promocode_assignment_promocode_id_foreign_key',
            ondelete='CASCADE',
        ),
    )
    is_refunded: Mapped[bool] = mapped_column(default=False, nullable=True)
