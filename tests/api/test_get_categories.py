import pytest


@pytest.mark.asyncio
async def test_get_categories(async_client):
    response = await async_client.get("/categories/")
    assert response.status_code == 200
