from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid
from typing import Any
from shop_app.database.database import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str] = mapped_column(nullable=False)
    is_disabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    groups: Mapped[list['Group']] = relationship(
        back_populates='group',
        secondary='group_product_assignment',
    )
    categories: Mapped[list['Category']] = relationship(
        back_populates='category',
        secondary='product_category_assignment',
    )
    tags: Mapped[list['Tag']] = relationship(
        back_populates='tag',
        secondary='product_tag_assignment',
    )
    marks: Mapped[list['Mark']] = relationship(
        back_populates='mark',
        secondary='product_mark_assignment',
    )
    product_characteristics: Mapped[list['Product_characteristic']] = relationship(
        back_populates='product_characteristic',
    )
    product_parameters: Mapped[list['Product_parameter']] = relationship(
        back_populates='product_parameter',
    )
    product_descriptions: Mapped[list['Product_description']] = relationship(
        back_populates='product_description',
    )


class ProductDescription(Base):
    __tablename__ = 'product_description'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'product.id',
            name='product_description_product_id_fk',
            ondelete='CASCADE',),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(default='Description', nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    sort_order: Mapped[int] = mapped_column(nullable=False)

    product: Mapped['Product'] = relationship(
        back_populates='product',
    )

class ProductParameter(Base):
    __tablename__ = 'product_parameter'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    is_main: Mapped[bool] = mapped_column(nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'product.id',
            name='product_parameter_product_id_fk',
            ondelete='CASCADE',
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
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(nullable=True)

    product: Mapped['Product'] = relationship(
        back_populates='product',
    )
    reviews: Mapped[list['Review']] = relationship(
        back_populates='review',
    )

class ProductCharacteristic(Base):
    # TODO: is_visible, is_for_filter validation
    __tablename__ = 'product_characteristic'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str] = mapped_column(nullable=False)
    text_value: Mapped[str | None] = mapped_column(nullable=True)
    num_value: Mapped[int | None] = mapped_column(nullable=True)
    sort_order: Mapped[int] = mapped_column(nullable=False)
    is_text_value: Mapped[bool] = mapped_column(nullable=False)
    is_visible: Mapped[bool] = mapped_column(nullable=False)
    is_for_filter: Mapped[bool] = mapped_column(nullable=False)
    unit_measurement_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'unit_measurement.id',
            name='product_characteristic_unit_measurement_id_fk',
            ondelete='CASCADE',
        ),
        nullable=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'product.id',
            name='product_characteristic_product_id_fk',
            ondelete='CASCADE',
        ),
        nullable=False,
    )

    unit_measurement: Mapped['UnitMeasurement'] = relationship(
        back_populates='unit_measurement',
    )
    product: Mapped['Product'] = relationship(
        back_populates='product',
    )
