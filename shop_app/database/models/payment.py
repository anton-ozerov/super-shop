import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base

if TYPE_CHECKING:
    from shop_app.database.models.order import Order


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    status: Mapped[str] = mapped_column(default="PENDING", nullable=False)
    foreign_id: Mapped[str | None] = mapped_column(nullable=True)
    payment_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    system: Mapped[str] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(
        back_populates="payment",
    )
