import uuid

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from shop_app.database.database import Base


class ProductCategoryAssignment(Base):
    __tablename__ = "product_category_assignment"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "product.id",
            name="product_category_assignment_product_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "category.id",
            name="product_category_assignment_category_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
