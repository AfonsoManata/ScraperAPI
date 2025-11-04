import pytest
from httpx import AsyncClient
from src.main import app

# This tests are just a starting point, in real life the testing needs to go deeper

@pytest.mark.asyncio
async def test_aptoide_missing_param():
    """
    Test: query param missing -> should return 422 validation error
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/aptoide")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_aptoide_invalid_param():
    """
    Test: invalid package name (bad characters) -> should return 422
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/aptoide?package_name=<script>bad</script>")

    assert response.status_code == 422

# Probably add tests: rate limit exceeded; normal situation...
