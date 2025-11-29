from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.feature import FeatureFlag
from app.models.user import User


class FeatureService:
    @staticmethod
    async def is_enabled(db: AsyncSession, feature_name: str, user: User = None) -> bool:
        # 1. 查数据库中的全局开关
        # (生产环境建议把这个结果缓存到 Redis，避免每次都查 DB)
        result = await db.execute(select(FeatureFlag).filter(FeatureFlag.name == feature_name))
        flag = result.scalars().first()

        if not flag:
            return False

        if flag.is_global_enabled:
            return True

        # 2. 如果全局没开，检查是不是超级管理员 (灰度测试)
        if user and user.is_superuser:
            return True

        return False