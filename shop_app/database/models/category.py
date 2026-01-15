import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base

if TYPE_CHECKING:
    from shop_app.database.models.product import Product


class Category(Base):
    __tablename__ = "category"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(nullable=False)
    parent_category_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "category.id",
            name="category_parent_category_id_fk",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    sort_order: Mapped[int] = mapped_column(nullable=False)

    parent_category: Mapped["Category"] = relationship(
        back_populates="category",
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="product",
        secondary="product_category_assignment",
    )
