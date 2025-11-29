from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# 依赖注入函数 (用于 API 接口获取 DB 会话)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session