import pytest


@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/health/check")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "Service is healthy and running"}
