from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB

import uuid
from typing import Any
from shop_app.database.database import Base


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    status: Mapped[str] = mapped_column(nullable=False)
    goods_info: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'user.id',
            name='order_user_id_fk',
            ondelete='CASCADE'),
        nullable=False,
    )
    payment_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'payment.id',
            name='order_payment_id_fk',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    delivery_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            'delivery.id',
            name='order_delivery_id_fk',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    comment: Mapped[str | None] = mapped_column(nullable=True)

    payment: Mapped['Payment'] = relationship(
        back_populates='payment',
    )
    delivery: Mapped['Delivery'] = relationship(
        back_populates='delivery',
    )
