from sqlalchemy import SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

import datetime
from shop_app.database.database import Base
from shop_app.enums import DiscountType


class Promocode(Base):
    __tablename__ = "promocode"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    quantity: Mapped[int]
    active_until_date: Mapped[datetime.datetime | None]
    is_combined_w_other_promotions: Mapped[bool] = mapped_column(default=False)
    how_many_times_per_user: Mapped[int] = mapped_column(SmallInteger)
    discount_type: Mapped[DiscountType]
    included_products_ids: Mapped[list[str] | None] = mapped_column(JSONB)
    excluded_products_ids: Mapped[list[str] | None] = mapped_column(JSONB)


class UserPromocodeAssignment(Base):
    __tablename__ = "user_promocode_assignment"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    promocode_id: Mapped[int]
    is_refunded: Mapped[bool] = mapped_column(default=False)

# Or included, or excluded?
# Not ready yet
