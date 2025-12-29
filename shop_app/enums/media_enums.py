import enum


class MediaType(enum.Enum):
    image = "image"
    video = "video"
    text = "text"
    audio = "audio"
    document = "document"


class MediaVariantFormat(enum.Enum):
    webp = "WEBP"
    jpg = "JPG"
    png = "PNG"


class EntityType(enum.Enum):
    product = "product"
    category = "category"
    review = "review"
