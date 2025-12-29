from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

import uuid
from shop_app.database.database import Base


class ProductMarkAssignment(Base):
    __tablename__ = 'product_mark_assignment'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'product.id',
            name='product_mark_assignment_product_id_fk',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    mark_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'mark.id',
            name='product_mark_assignment_mark_id_fk',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
