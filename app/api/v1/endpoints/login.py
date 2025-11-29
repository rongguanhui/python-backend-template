from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api import deps
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse

router = APIRouter()


# 1. 登录接口 (获取 Token)
@router.post("/login/access-token", response_model=Token)
async def login_access_token(
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # 查找用户
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()

    # 校验密码
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # 生成 Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.email, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


# 2. 注册接口
@router.post("/signup", response_model=UserResponse)
async def create_user(
        *,
        db: AsyncSession = Depends(get_db),
        user_in: UserCreate,
) -> Any:
    # 检查邮箱是否已存在
    result = await db.execute(select(User).filter(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    # 创建新用户
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# 3. 测试接口：获取当前用户信息 (需要登录)
@router.get("/me", response_model=UserResponse)
async def read_users_me(
        current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user