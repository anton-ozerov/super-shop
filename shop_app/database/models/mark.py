import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base

if TYPE_CHECKING:
    from shop_app.database.models.product import Product


class Mark(Base):
    __tablename__ = "mark"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(nullable=False)
    banner_color_code: Mapped[str] = mapped_column(String(8), default="#FFFFFF", nullable=False)
    text_color_code: Mapped[str] = mapped_column(String(8), default="#000000", nullable=False)
    is_visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    products: Mapped[list["Product"]] = relationship(
        back_populates="product",
        secondary="product_mark_assignment",
    )
