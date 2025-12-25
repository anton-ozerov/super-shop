from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from shop_app.database.database import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_disabled: Mapped[bool] = mapped_column(default=False)
    sort_order: Mapped[int]
    is_deleted: Mapped[bool] = mapped_column(default=False)
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB)


class ProductDescription(Base):
    __tablename__ = 'product_description'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(default='Description')
    value: Mapped[str]
    sort_order: Mapped[int]

# Not ready yet
