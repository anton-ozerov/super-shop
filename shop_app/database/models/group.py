import uuid
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base

if TYPE_CHECKING:
    from shop_app.database.models.product import Product


class Group(Base):
    __tablename__ = "group"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str | None] = mapped_column(nullable=True)

    products: Mapped[list["Product"]] = relationship(
        back_populates="product",
        secondary="group_product_assignment",
    )
