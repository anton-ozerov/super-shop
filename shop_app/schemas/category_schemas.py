from uuid import UUID

from pydantic import BaseModel, Field

from .pagination_schemas import PaginationSchema


class CategoryOut(BaseModel):
    id: UUID = Field(
        ...,
        description="Unique ID for each category",
    )
    name: str = Field(
        ...,
        description="Name of the category",
    )
    parent_category_id: UUID | None = None
    sort_order: int = Field(
        ...,
        description="Order in the sorting",
    )

    class Config:
        from_attributes = True


class CategoriesAll(BaseModel):
    status: bool = True
    pagination: PaginationSchema = Field(
        ...,
        description="Pagination description",
    )
    message: str = "All categories received successfully"
    categories: list[CategoryOut] = []
