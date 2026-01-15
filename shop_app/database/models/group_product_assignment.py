import uuid

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from shop_app.database.database import Base


class GroupProductAssignment(Base):
    __tablename__ = "group_product_assignment"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("group.id", name="group_product_assignment_group_id_fk", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("product.id", name="group_product_assignment_product_id_fk", ondelete="CASCADE"),
        nullable=False,
    )
    product_value: Mapped[str] = mapped_column(nullable=False)
