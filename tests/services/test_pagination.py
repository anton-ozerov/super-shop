from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from shop_app.services.product_service import get_pagination


@pytest.mark.parametrize(
    (
        "total_items",
        "per_page",
        "page",
        "current_items",
        "expected_total_pages",
        "expected_has_next",
        "expected_has_previous",
        "expected_exception_type",
    ),
    [
        (50, 10, 1, 10, 5, True, False, None),  # First page
        (50, 10, 2, 10, 5, True, True, None),  # Middle page
        (50, 10, 5, 10, 5, False, True, None),  # Last page
        (50, 10, 6, 0, 5, False, True, None),  # Page after last
        (0, 10, 1, 0, 0, False, False, None),  # No items
        (7, 10, 1, 7, 1, False, False, None),  # Fewer items than per_page
        (25, 10, 3, 5, 3, False, True, None),  # Last page with fewer items
        (-10, 10, 1, 0, 0, False, False, pydantic.ValidationError),  # Negative total items
        (50, -1, 0, 0, 0, False, False, pydantic.ValidationError),  # Negative per_page
        (50, 10, -2, 0, 0, False, False, pydantic.ValidationError),  # Negative page number
        (50, 10, 1, 5, 5, True, False, None),  # Mismatched current_items
    ],
)
def test_pagination(
    total_items: int,
    per_page: int,
    page: int,
    current_items: int,
    expected_total_pages: int,
    expected_has_next: bool,
    expected_has_previous: bool,
    expected_exception_type: type[BaseException] | None,
):
    expectation = pytest.raises(expected_exception_type) if expected_exception_type is not None else does_not_raise()
    with expectation as exc_info:
        pagination = get_pagination(total_items=total_items, per_page=per_page, page=page, current_items=current_items)

    if exc_info is None:
        assert pagination.total_items == total_items
        assert pagination.per_page == per_page
        assert pagination.page == page
        assert pagination.current_items == current_items
        assert pagination.total_pages == expected_total_pages
        assert pagination.has_next == expected_has_next
        assert pagination.has_previous == expected_has_previous
    else:
        assert exc_info.type is expected_exception_type
