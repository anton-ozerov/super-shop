from pydantic import BaseModel, Field


class PaginationSchema(BaseModel):
    page: int = Field(..., description="Page number", ge=1)
    total_pages: int = Field(..., description="Total number of pages", ge=0)
    per_page: int = Field(..., description="Number of items per page", ge=1, le=200)
    total_items: int = Field(..., description="Total number of items", ge=0)
    current_items: int = Field(..., description="Number of items on the current page", ge=0, le=200)
    has_next: bool = Field(..., description="Indicates if there is a next page")
    has_previous: bool = Field(..., description="Indicates if there is a previous page")
