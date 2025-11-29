import pytest
from app.core.config import settings

@pytest.mark.asyncio
async def test_create_product_without_login(client): # <--- 直接注入 client
    response = await client.post(
        f"{settings.API_V1_STR}/products/",
        json={"title": "test", "sku": "test_001", "price": 10.0}
    )
    assert response.status_code == 400