from pydantic import BaseModel, EmailStr
from typing import Optional


# 共享属性
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    full_name: Optional[str] = None


# 注册时用
class UserCreate(UserBase):
    password: str


# 数据库返回用
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# Token 响应格式
class Token(BaseModel):
    access_token: str
    token_type: str