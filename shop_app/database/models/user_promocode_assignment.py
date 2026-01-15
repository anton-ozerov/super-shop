import uuid

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from shop_app.database.database import Base


class UserPromocodeAssignment(Base):
    __tablename__ = "user_promocode_assignment"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "user.id",
            name="user_promocode_assignment_user_id_foreign_key",
            ondelete="CASCADE",
        ),
    )
    promocode_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "promocode.id",
            name="user_promocode_assignment_promocode_id_foreign_key",
            ondelete="CASCADE",
        ),
    )
    is_refunded: Mapped[bool] = mapped_column(default=False, nullable=False)
