from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from shop_app.database.database import Base


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_category_id: Mapped[int | None] = mapped_column(
        ForeignKey('category.id', ondelete='CASCADE'),
    )
    sort_order: Mapped[int]


class ProductCategoryAssignment(Base):
    __tablename__ = 'product_category_assignment'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE'),
        primary_key=True,
    )

# Not ready yet
