import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base

if TYPE_CHECKING:
    from shop_app.database.models.product import ProductCharacteristic


class UnitMeasurement(Base):
    __tablename__ = "unit_measurement"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    short_name: Mapped[str] = mapped_column(nullable=False)
    min_unit_measurement_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "unit_measurement.id",
            name="unit_measurement_min_unit_measurement_id_fk",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    quantity_in_min_unit: Mapped[int | None] = mapped_column(nullable=True)

    product_characteristics: Mapped[list["ProductCharacteristic"]] = relationship(
        back_populates="product_characteristic",
    )
