import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from app.main import app

# 1. 解决 event_loop 问题 (针对 pytest-asyncio)
@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    # 这里封装好了 transport 逻辑，以后测试用例里直接用 client 就行
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac