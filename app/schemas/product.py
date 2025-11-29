from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


# 1. 基础字段 (请求和响应共有的)
class ProductBase(BaseModel):
    title: str
    sku: str
    price: float = 0.0
    currency: str = "USD"
    stock_qty: int = 0
    description_original: Optional[str] = None
    source_url: Optional[str] = None
    supplier_cost: float = 0.0


# 2. 创建时需要的字段
class ProductCreate(ProductBase):
    pass


# 3. 响应时返回的字段 (包含 ID, 创建时间, AI 字段)
class ProductResponse(ProductBase):
    id: int
    status: str

    # --- 这里是修正的关键 ---
    # 数据库里叫 is_ai_optimized，这里也必须叫这个名字
    is_ai_optimized: bool
    description_ai: Optional[str] = None
    seo_keywords: Optional[str] = None

    # 图片字段 (数据库是 JSON，Pydantic 会自动转为 List)
    images: Optional[List[str]] = None
    video_url: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    # 允许从 ORM 对象读取数据 (旧版叫 orm_mode = True)
    model_config = ConfigDict(from_attributes=True)