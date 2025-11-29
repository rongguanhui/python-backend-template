from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog

class AuditService:
    @staticmethod
    async def log(
        db: AsyncSession,
        user_id: int,
        action: str,
        resource: str,
        resource_id: str,
        details: dict = None,
        ip: str = None
    ):
        audit = AuditLog(
            user_id=user_id,
            action=action,
            target_resource=resource,
            target_id=str(resource_id),
            details=details,
            ip_address=ip
        )
        db.add(audit)
        # 注意：这里不commit，跟随业务主事务一起commit，或者手动commit
        # await db.commit()