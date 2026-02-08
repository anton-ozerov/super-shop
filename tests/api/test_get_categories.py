from math import ceil

import pytest

from shop_app.database import Category


@pytest.mark.asyncio
async def test_get_categories(async_client):
    """Getting categories test, no categories in database. Default pagination params test"""
    response = await async_client.get("/categories/")
    data = response.json()

    assert "status" in data
    assert "pagination" in data
    assert "message" in data
    assert "categories" in data

    assert data["status"] is True
    assert data["message"] == "No categories found"
    assert len(data["categories"]) == 0

    pagination = data["pagination"]
    assert pagination["page"] == 1
    assert pagination["total_pages"] == 0
    assert pagination["per_page"] == 10
    assert pagination["total_items"] == 0
    assert pagination["current_items"] == 0
    assert pagination["has_next"] is False
    assert pagination["has_previous"] is False


@pytest.mark.asyncio
async def test_create_categories(async_client, db_session):
    """Creating categories test"""
    categories = {
        Category(
            name="Test1",
            sort_order=1,
        ),
        Category(
            name="Test2",
            sort_order=2,
        ),
        Category(
            name="Test3",
            sort_order=3,
        ),
    }

    db_session.add_all(categories)
    await db_session.commit()

    response = await async_client.get("/categories/")
    data = response.json()

    assert response.status_code == 200
    assert len(data["categories"]) == 3

    cat_number = 0
    for cat in data["categories"]:
        cat_number += 1
        assert cat["name"] == "Test" + str(cat_number)
        assert cat["sort_order"] == cat_number

    assert data["message"] == "Found 3 categories"


@pytest.mark.asyncio
async def test_parent_category(async_client, db_session):
    """Valid parent category test"""
    parent_category = Category(
        name="Parent",
        sort_order=1,
    )

    db_session.add(parent_category)
    await db_session.commit()

    parent_uuid = parent_category.id

    child_category = Category(
        name="Child",
        parent_category_id=parent_uuid,
        sort_order=2,
    )

    db_session.add(child_category)
    await db_session.commit()

    response = await async_client.get("/categories/")
    data = response.json()

    assert response.status_code == 200
    assert len(data["categories"]) == 2

    assert data["categories"][1]["parent_category_id"] == str(parent_uuid)


@pytest.mark.asyncio
async def test_category_simple_pagination(async_client, db_session):
    """Simple pagination test"""
    categories = set()
    total_items = 7
    for i in range(total_items):
        cat = Category(
            name="Test" + str(i),
            sort_order=i,
        )
        categories.add(cat)
    db_session.add_all(categories)
    await db_session.commit()

    page = 2
    per_page = 3
    current_items = min(per_page, total_items - (page - 1) * per_page)
    current_items = max(0, current_items)
    response = await async_client.get(f"/categories/?page={page}&per_page={per_page}")
    data = response.json()

    assert response.status_code == 200

    pagination = data["pagination"]

    assert pagination["page"] == page
    assert pagination["total_pages"] == ceil(total_items / per_page)
    assert pagination["per_page"] == per_page
    assert pagination["total_items"] == total_items
    assert pagination["current_items"] == current_items
    assert pagination["has_next"] is True
    assert pagination["has_previous"] is True


@pytest.mark.asyncio
async def test_category_pagination_boundary(async_client, db_session):
    """Pagination boundary test"""
    categories = set()
    total_items = 10
    for i in range(total_items):
        cat = Category(
            name="Test" + str(i),
            sort_order=i,
        )
        categories.add(cat)
    db_session.add_all(categories)
    await db_session.commit()

    page = 1
    per_page = 3
    total_pages = ceil(total_items / per_page)
    current_items = min(per_page, total_items - (page - 1) * per_page)
    current_items = max(0, current_items)
    response1 = await async_client.get(f"/categories/?page={page}&per_page={per_page}")
    data1 = response1.json()

    pagination1 = data1["pagination"]
    assert pagination1["page"] == page
    assert pagination1["total_pages"] == total_pages
    assert pagination1["per_page"] == per_page
    assert pagination1["total_items"] == total_items
    assert pagination1["current_items"] == current_items
    assert pagination1["has_next"] is True
    assert pagination1["has_previous"] is False

    page = 4
    per_page = 3
    total_pages = ceil(total_items / per_page)
    current_items = min(per_page, total_items - (page - 1) * per_page)
    current_items = max(0, current_items)
    response2 = await async_client.get(f"/categories/?page={page}&per_page={per_page}")
    data2 = response2.json()

    pagination2 = data2["pagination"]
    assert pagination2["page"] == page
    assert pagination2["total_pages"] == total_pages
    assert pagination2["per_page"] == per_page
    assert pagination2["total_items"] == total_items
    assert pagination2["current_items"] == current_items
    assert pagination2["has_next"] is False
    assert pagination2["has_previous"] is True


@pytest.mark.asyncio
async def test_category_pagination_invalid_params(async_client, db_session):
    """Invalid params test"""
    category = Category(
        name="Test",
        sort_order=1,
    )
    db_session.add(category)
    await db_session.commit()

    total_items = 1
    page = 2
    per_page = 3
    total_pages = ceil(total_items / per_page)
    current_items = min(per_page, total_items - (page - 1) * per_page)
    current_items = max(0, current_items)
    response = await async_client.get(f"/categories/?page={page}&per_page={per_page}")
    data = response.json()

    assert response.status_code == 200

    pagination = data["pagination"]
    assert pagination["page"] == page
    assert pagination["total_pages"] == total_pages
    assert pagination["per_page"] == per_page
    assert pagination["total_items"] == total_items
    assert pagination["current_items"] == current_items
    assert pagination["has_next"] is False
    assert pagination["has_previous"] is True


@pytest.mark.asyncio
async def test_category_pagination_out_of_range(async_client):
    """Out-of-range pagination params test"""
    page = -1
    response1 = await async_client.get(f"/categories/?page={page}")
    assert response1.status_code == 422

    per_page = 0
    response2 = await async_client.get(f"/categories/?per_page={per_page}")
    assert response2.status_code == 422

    per_page = 101
    response3 = await async_client.get(f"/categories/?per_page={per_page}")
    assert response3.status_code == 422
