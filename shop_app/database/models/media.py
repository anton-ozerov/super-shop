from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from typing import Any
from shop_app.database.database import Base
from shop_app.enums import MediaType, MediaVariantFormat, EntityType


class Media(Base):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType]
    original_url: Mapped[str]
    mime_type: Mapped[str]
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB)


class MediaVariant(Base):
    __tablename__ = 'media_variant'

    id: Mapped[int] = mapped_column(primary_key=True)
    media_id: Mapped[int] = mapped_column(
        ForeignKey('media.id', ondelete='CASCADE'),
    )
    url: Mapped[str]
    width: Mapped[int | None]
    height: Mapped[int | None]
    quality: Mapped[int | None] = mapped_column(SmallInteger)
    format: Mapped[MediaVariantFormat]
    size_bytes: Mapped[int]
    role: Mapped[str]
    additional_info: Mapped[dict[str, Any] | None] = mapped_column(JSONB)


class MediaLink(Base):
    __tablename__ = 'media_link'

    id: Mapped[int] = mapped_column(primary_key=True)
    media_id: Mapped[int] = mapped_column(
        ForeignKey('media.id', ondelete='CASCADE'),
    )
    entity_type: Mapped[EntityType]
    entity_id: Mapped[int]
    alt_text: Mapped[str]
    role: Mapped[str]
    sort_order: Mapped[int]

# Entity_id? Entity_type?
