from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ResponseSchema(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None

# 辅助函数，用于快速返回标准格式
def success(data: T = None, message: str = "success"):
    return {"code": 200, "message": message, "data": data}

def fail(code: int = 400, message: str = "error", data: T = None):
    return {"code": code, "message": message, "data": data}