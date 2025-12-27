from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import text

import uuid
from shop_app.database.database import Base


class UnitMeasurement(Base):
    __tablename__ = 'unit_measurement'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    short_name: Mapped[str] = mapped_column(nullable=False)
    min_unit_measurement_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    quantity_in_min_unit: Mapped[int] = mapped_column(nullable=True)

    product_characteristics: Mapped[list['ProductCharacteristic']] = relationship(
        back_populates='product_characteristic',
    )
