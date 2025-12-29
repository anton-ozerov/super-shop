from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

import uuid
from shop_app.database.database import Base


class ProductTag(Base):
    __tablename__ = 'product_tag'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'product.id',
            name='product_tag_product_id_fk',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'tag.id',
            name='product_tag_tag_id_fk',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
