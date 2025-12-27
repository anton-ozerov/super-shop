from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

import uuid
from shop_app.database.database import Base


class Group(Base):
    __tablename__ = 'group'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str | None] = mapped_column(nullable=True)

    products: Mapped[list['Product']] = relationship(
        back_populates='product',
        secondary='group_product_assignment',
    )


class GroupProductAssignment(Base):
    __tablename__ = 'group_product_assignment'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'group.id',
            name='group_product_assignment_group_id_fk',
            ondelete='CASCADE'),
        nullable=False,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'product.id',
            name='group_product_assignment_product_id_fk',
            ondelete='CASCADE'),
        nullable=False,
    )
    product_value: Mapped[str] = mapped_column(nullable=False)
