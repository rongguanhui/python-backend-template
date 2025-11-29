from datetime import datetime
from sqlalchemy import Integer, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=True) # 可能有系统自动操作
    action: Mapped[str] = mapped_column(String(50), comment="CREATE/UPDATE/DELETE")
    target_resource: Mapped[str] = mapped_column(String(50), comment="User/Product")
    target_id: Mapped[str] = mapped_column(String(50), comment="被操作对象的ID")
    details: Mapped[dict] = mapped_column(JSON, nullable=True, comment="修改前后的快照")
    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())