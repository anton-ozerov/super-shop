from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

import uuid
from shop_app.database.database import Base


class Mark(Base):
    __tablename__ = 'mark'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str] = mapped_column(nullable=False)
    color_code: Mapped[str] = mapped_column(default='#FFFFFF', nullable=False)
    is_visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    products: Mapped[list['Product']] = relationship(
        back_populates='product',
        secondary='product_mark_assignment',
    )
