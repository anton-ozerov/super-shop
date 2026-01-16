import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base

if TYPE_CHECKING:
    from shop_app.database.models.category import Category
    from shop_app.database.models.group import Group
    from shop_app.database.models.mark import Mark
    from shop_app.database.models.review import Review
    from shop_app.database.models.tag import Tag
    from shop_app.database.models.unit_measurement import UnitMeasurement


class Product(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(nullable=False)
    is_disabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    groups: Mapped[list["Group"]] = relationship(
        back_populates="group",
        secondary="group_product_assignment",
    )
    categories: Mapped[list["Category"]] = relationship(
        back_populates="products",
        secondary="product_category_assignment",
    )
    tags: Mapped[list["Tag"]] = relationship(
        back_populates="tag",
        secondary="product_tag_assignment",
    )
    marks: Mapped[list["Mark"]] = relationship(
        back_populates="mark",
        secondary="product_mark_assignment",
    )
    product_characteristics: Mapped[list["ProductCharacteristic"]] = relationship(
        back_populates="product_characteristic",
    )
    product_parameters: Mapped[list["ProductParameter"]] = relationship(
        back_populates="product_parameter",
    )
    product_descriptions: Mapped[list["ProductDescription"]] = relationship(
        back_populates="product_description",
    )


class ProductDescription(Base):
    __tablename__ = "product_description"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "product.id",
            name="product_description_product_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(default="Description", nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    sort_order: Mapped[int] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship(
        back_populates="product",
    )


class ProductParameter(Base):
    __tablename__ = "product_parameter"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    is_main: Mapped[bool] = mapped_column(nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "product.id",
            name="product_parameter_product_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    old_price: Mapped[int] = mapped_column(nullable=False)
    quantity_in_warehouse: Mapped[int] = mapped_column(nullable=False)
    quantity_in_postpone: Mapped[int] = mapped_column(nullable=False)
    is_infinite: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_disabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(nullable=False)
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    product: Mapped["Product"] = relationship(
        back_populates="product",
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="review",
    )


class ProductCharacteristic(Base):
    __tablename__ = "product_characteristic"

    __table_args__ = (
        CheckConstraint(
            "NOT (is_visible = false AND is_for_filter = false)",
            name="check_visible_filter_characteristic",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(nullable=False)
    text_value: Mapped[str | None] = mapped_column(nullable=True)
    num_value: Mapped[int | None] = mapped_column(nullable=True)
    sort_order: Mapped[int] = mapped_column(nullable=False)
    is_text_value: Mapped[bool] = mapped_column(nullable=False)
    is_visible: Mapped[bool] = mapped_column(nullable=False)
    is_for_filter: Mapped[bool] = mapped_column(nullable=False)
    unit_measurement_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "unit_measurement.id",
            name="product_characteristic_unit_measurement_id_fk",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "product.id",
            name="product_characteristic_product_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    unit_measurement: Mapped["UnitMeasurement"] = relationship(
        back_populates="unit_measurement",
    )
    product: Mapped["Product"] = relationship(
        back_populates="product",
    )
