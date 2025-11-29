from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Float, Boolean, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy import ForeignKey


class Product(Base):
    __tablename__ = "products"

    # 1. 新增：所有者ID (外键关联 User 表)
    # nullable=False 表示这个商品必须属于某个人
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="所属用户ID")
    # 1. 基础信息 (Basic Info)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment="本地唯一的SKU")
    title: Mapped[str] = mapped_column(String(255), index=True, comment="商品标题")
    price: Mapped[float] = mapped_column(Float, default=0.0, comment="建议售价")
    currency: Mapped[str] = mapped_column(String(10), default="USD", comment="货币单位")
    stock_qty: Mapped[int] = mapped_column(Integer, default=0, comment="本地库存数量")

    # 2. AI 内容与优化 (AI & Content)
    # 为什么要分 original 和 ai ? 为了方便重新生成，对比效果。
    description_original: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="原始采集的描述")
    description_ai: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="AI 重写后的营销描述")
    seo_keywords: Mapped[Optional[str]] = mapped_column(String(500), nullable=True,
                                                        comment="AI 生成的SEO关键词,逗号分隔")
    is_ai_optimized: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否已完成AI优化")

    # 3. 多媒体资源 (Media)
    # 使用 PostgreSQL 的 JSON 类型存储图片列表，比关联表更轻量
    images: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True,
                                                        comment="图片URL列表 ['http://...', 'http://...']")
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="AI 生成的短视频地址")

    # 4. 供应链信息 (Supply Chain)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True,
                                                      comment="采购来源URL (如 AliExpress/1688)")
    supplier_cost: Mapped[float] = mapped_column(Float, default=0.0, comment="采购成本价")

    # 5. 状态与审计 (Status & Audit)
    status: Mapped[str] = mapped_column(String(20), default="draft", comment="状态: draft, published, archived")

    # 自动记录时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())

    def __repr__(self):
        return f"<Product(sku={self.sku}, title={self.title})>"