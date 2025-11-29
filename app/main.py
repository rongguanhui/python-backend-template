from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import engine
from app.models.product import Base
from app.core.logger import setup_logging
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis_limit
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis # 注意：fastapi-cache2 依赖 redis-py 的 async

# 1. 配置日志
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("系统启动中...")
    # 自动建表 (仅开发环境使用，生产环境请用 Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("数据库连接成功")

    # 连接 Redis 做限流
    redis_connection = redis_limit.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)

    # --- 缓存初始化开始 ---
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info("Redis 缓存系统已挂载")
    # --- 缓存初始化结束 ---

    yield

    logger.info("系统关闭中...")
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# 2. 注册异常处理器 (Exception Handlers)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 3. 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"], # 生产环境千万别写 "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 限制 Host 头，防止 HTTP Host Header 攻击
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "your-domain.com"]
)


@app.get("/")
def root():
    logger.info("有人访问了首页")  # 测试日志
    return {"message": "SaaS AI Backend is Running!"}
@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "ok",
        "db": "connected",
        "redis": "connected"
    }