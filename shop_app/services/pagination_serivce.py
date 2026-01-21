import logging

from shop_app.schemas import PaginationSchema

logger = logging.getLogger(__name__)


def calculate_pagination(
    total_items: int,
    items_per_page: int,
    current_page: int,
    current_count_items: int,
) -> PaginationSchema:
    """Calculate pagination details based on total items, items per page, and current page"""
    total_pages = (total_items + items_per_page - 1) // items_per_page
    has_previous = current_page > 1
    has_next = current_page < total_pages

    current_items_in_theory = min(items_per_page, total_items - (current_page - 1) * items_per_page)
    if current_count_items != current_items_in_theory:
        logger.warning(
            "Current count items does not match theoretical count",
            extra={
                "service": "pagination_service",
                "method": "calculate_pagination",
                "total_items": total_items,
                "items_per_page": items_per_page,
                "current_page": current_page,
                "current_count_items": current_count_items,
                "theoretical_count_items": current_items_in_theory,
            },
        )

    res = PaginationSchema(
        page=current_page,
        total_pages=total_pages,
        per_page=items_per_page,
        total_items=total_items,
        current_items=current_count_items,
        has_next=has_next,
        has_previous=has_previous,
    )

    return res
