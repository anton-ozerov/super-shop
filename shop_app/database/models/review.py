import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base

if TYPE_CHECKING:
    from shop_app.database.models.product import ProductParameter
    from shop_app.database.models.user import User


class Review(Base):
    __tablename__ = "review"

    __table_args__ = CheckConstraint(
        "stars >= 1 and stars <= 5",
        name="check_review_stars",
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[int | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "user.id",
            name="review_user_id_fk",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    parameter_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "parameter.id",
            name="review_parameter_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    stars: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    comment: Mapped[str | None] = mapped_column(nullable=True)

    product_parameter: Mapped["ProductParameter"] = relationship(
        back_populates="product_parameter",
    )
    user: Mapped["User"] = relationship(
        back_populates="user",
    )
