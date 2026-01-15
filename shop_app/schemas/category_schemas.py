from uuid import UUID

from pydantic import BaseModel, Field


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
    message: str = "All categories received successfully"
    categories: list[CategoryOut] = []
    total_count: int = 0
