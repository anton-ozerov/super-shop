import uuid
from typing import Any

from sqlalchemy import ForeignKey, SmallInteger, text
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shop_app.database.database import Base
from shop_app.enums import EntityType, MediaType, MediaVariantFormat


class Media(Base):
    __tablename__ = "media"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )
    type: Mapped[MediaType] = mapped_column(
        ENUM(
            MediaType,
            name="media_type_enum",
            check_constraint=True,
        ),
        nullable=False,
    )
    original_url: Mapped[str] = mapped_column(nullable=False)
    mime_type: Mapped[str] = mapped_column(nullable=False)
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    media_variants: Mapped[list["MediaVariant"]] = relationship(
        back_populates="media_variant",
    )
    media_links: Mapped[list["MediaLink"]] = relationship(
        back_populates="media_link",
    )


class MediaVariant(Base):
    __tablename__ = "media_variant"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    media_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("media.id", name="media_variant_media_id_fk", ondelete="CASCADE"),
        nullable=False,
    )
    url: Mapped[str] = mapped_column(nullable=False)
    width: Mapped[int | None] = mapped_column(nullable=True)
    height: Mapped[int | None] = mapped_column(nullable=True)
    quality: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    format: Mapped[MediaVariantFormat] = mapped_column(
        ENUM(
            MediaVariantFormat,
            name="media_variant_enum",
            check_constraint=True,
        ),
        nullable=False,
    )
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    media: Mapped["Media"] = relationship(
        back_populates="media",
    )


class MediaLink(Base):
    __tablename__ = "media_link"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    media_id: Mapped[int] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "media.id",
            name="media_link_media_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    entity_type: Mapped[EntityType] = mapped_column(
        ENUM(
            EntityType,
            name="entity_type_enum",
            check_constraint=True,
        ),
        nullable=False,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
    )
    alt_text: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    sort_order: Mapped[int] = mapped_column(nullable=False)

    media: Mapped["Media"] = relationship(
        back_populates="media",
    )
