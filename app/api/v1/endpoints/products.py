from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.api import deps
from app.db.session import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse
from app.services.audit import AuditService
from app.services.data_processing import DataService

# 如果你有定义 ProductUpdate Schema，也可以引入，这里暂时用 ProductCreate 代替或新建一个

router = APIRouter()


# 1. 获取产品列表 (只返回当前用户的产品)
@router.get("/", response_model=List[ProductResponse])
async def read_products(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(deps.get_current_user)  # <--- 必须登录
):
    # 核心逻辑：增加 .filter(Product.owner_id == current_user.id)
    query = select(Product).filter(Product.owner_id == current_user.id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# 2. 创建产品 (自动绑定当前用户)
@router.post("/", response_model=ProductResponse)
async def create_product(
        item: ProductCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(deps.get_current_user)
):
    # 将 Pydantic 对象转为字典，并额外注入 owner_id
    product_data = item.model_dump()
    new_product = Product(**product_data, owner_id=current_user.id)

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    # 这里可以继续加 Celery 任务触发 AI
    # generate_ai_content_task.delay(new_product.id, new_product.title)

    return new_product


# 3. 获取单个产品详情 (需校验权限)
@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(deps.get_current_user)
):
    query = select(Product).filter(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 严防越权访问：如果这个商品不是你的，报错！
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this product")

    return product


# 4. 更新产品
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
        product_id: int,
        item: ProductCreate,  # 实际开发建议单独定义 ProductUpdate，字段全是 Optional
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(deps.get_current_user)
):
    # 先查出来
    query = select(Product).filter(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 更新字段
    update_data = item.model_dump(exclude_unset=True)  # 只更新传进来的字段
    for key, value in update_data.items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


# 5. 删除产品
@router.delete("/{product_id}", status_code=204)
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(deps.get_current_user)
):
    query = select(Product).filter(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await db.delete(product)

    # 记录审计
    await AuditService.log(
        db=db,
        user_id=current_user.id,
        action="DELETE",
        resource="Product",
        resource_id=product_id,
        ip="127.0.0.1"
    )

    await db.commit()
    return None  # 204 No Content 不需要返回 body


# 1. 批量导入
@router.post("/import/excel")
async def import_products(
        file: UploadFile,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(deps.get_current_user)
):
    # 解析 Excel
    items = await DataService.parse_excel(file)

    # 批量入库 (Bulk Insert)
    # 注意：这里需要处理数据校验，如果数据量大建议扔给 Celery
    products_to_add = []
    for item in items:
        products_to_add.append(Product(
            title=item.get("Title"),
            sku=item.get("SKU"),
            price=float(item.get("Price", 0)),
            owner_id=current_user.id
        ))

    db.add_all(products_to_add)
    await db.commit()

    return {"message": f"成功导入 {len(items)} 条数据"}


# 2. 批量导出
@router.get("/export/excel")
async def export_products(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(deps.get_current_user)
):
    # 查出数据
    query = select(Product).filter(Product.owner_id == current_user.id)
    result = await db.execute(query)
    products = result.scalars().all()

    # 转为字典列表 (利用 Pydantic 的 model_dump)
    data = [ProductResponse.model_validate(p).model_dump() for p in products]

    # 生成 Excel 流
    excel_file = DataService.export_excel(data)

    # 返回文件流供浏览器下载
    headers = {'Content-Disposition': 'attachment; filename="products.xlsx"'}
    return StreamingResponse(excel_file, headers=headers,
                             media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')