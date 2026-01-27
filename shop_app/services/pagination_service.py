import logging
from math import ceil

from shop_app.schemas import PaginationSchema

logger = logging.getLogger(__name__)


def get_pagination(
    total_items: int,
    page: int,
    per_page: int,
    current_items: int,
) -> PaginationSchema:
    """Get pagination details based on total items, items per page, and current page"""
    if total_items < 1:
        return PaginationSchema(
            page=page,
            total_pages=0,
            per_page=per_page,
            total_items=0,
            current_items=0,
            has_next=False,
            has_previous=False,
        )

    total_pages = ceil(total_items / per_page)

    has_next = page < total_pages
    has_previous = (page > 1) and (page <= total_pages + 1)

    current_items_in_theory = min(per_page, total_items - (page - 1) * per_page)

    if current_items != current_items_in_theory:
        logger.warning(
            "Current count items does not match theoretical count",
            extra={
                "service": "pagination_service",
                "method": "get_pagination",
                "total_items": total_items,
                "per_page": per_page,
                "page": page,
                "current_items": current_items,
                "theoretical_count_items": current_items_in_theory,
            },
        )

    return PaginationSchema(
        page=page,
        total_pages=total_pages,
        per_page=per_page,
        total_items=total_items,
        current_items=current_items,
        has_next=has_next,
        has_previous=has_previous,
    )
