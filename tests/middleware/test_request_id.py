import pytest


@pytest.mark.asyncio
async def test_request_id_generated(async_client):
    response = await async_client.get("/health/check")

    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


@pytest.mark.asyncio
async def test_request_id_passthrough(async_client):
    response = await async_client.get(
        "/health/check",
        headers={"X-Request-ID": "test-id-123"},
    )

    assert response.headers["X-Request-ID"] == "test-id-123"
