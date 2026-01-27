from typing import Any

from pydantic import BaseModel, Field, field_validator

from shop_app.schemas._validating_id_as_uuid import validate_id_as_uuid
from shop_app.schemas.mark_schemas import MarkOut
from shop_app.schemas.pagination_schemas import PaginationSchema


class ProductOut(BaseModel):
    id: str = Field(..., description="Unique identifier of the user in UUIDv4 format")
    name: str = Field(..., description="Name of the product")
    description: str | None = Field(None, description="Description of the product")

    marks: list[MarkOut] = Field(..., description="List of marks associated with the product")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> str:
        """Validate that ID is a valid UUIDv4 string"""
        return validate_id_as_uuid(v_id=v)


class RepositoryGetNotDeletedProducts(BaseModel):
    total_count: int
    current_count: int
    products: list[ProductOut]


class GetProductsResponseSchema(BaseModel):
    products: list[ProductOut]
    pagination: PaginationSchema
