from pydantic import BaseModel


class PaginationSchema(BaseModel):
    page: int = 1
    total_pages: int = 1
    per_page: int = 10
    total_items: int = 10
    current_items: int = 10
    has_next: bool = False
    has_previous: bool = True
