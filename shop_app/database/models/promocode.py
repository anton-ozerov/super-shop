import datetime
import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, SmallInteger, text
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base
from shop_app.enums import DiscountType

if TYPE_CHECKING:
    from shop_app.database.models.user import User


class Promocode(Base):
    __tablename__ = "promocode"

    __table_args__ = (
        CheckConstraint(
            "NOT (included_products_ids IS NOT NULL AND excluded_products_ids IS NOT NULL)",
            name="check_promocode",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    value: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    active_until_date: Mapped[datetime.datetime | None] = mapped_column(nullable=True)
    is_combined_w_other_promotions: Mapped[bool] = mapped_column(default=False, nullable=False)
    how_many_times_per_user: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    discount_type: Mapped[DiscountType] = mapped_column(
        ENUM(
            DiscountType,
            name="discount_type_enum",
            check_constraint=True,
        ),
        nullable=False,
    )
    included_products_ids: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True)
    excluded_products_ids: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True)

    users: Mapped["User"] = relationship(
        back_populates="promocodes",
        secondary="user_promocode_assignment",
    )
