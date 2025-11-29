from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger

# 1. 处理 HTTP 错误 (如 404 Not Found, 403 Forbidden)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP Error: {exc.status_code} - {exc.detail} - URL: {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail, "data": None},
    )

# 2. 处理参数校验错误 (Pydantic 报错)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 把复杂的 Pydantic 错误简化成字符串
    error_msg = "; ".join([f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors()])
    logger.warning(f"Validation Error: {error_msg} - Body: {exc.body}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": 422, "message": f"参数校验失败: {error_msg}", "data": None},
    )

# 3. 处理所有未知的 500 错误 (兜底方案)
async def general_exception_handler(request: Request, exc: Exception):
    # 记录详细堆栈信息到日志文件 (非常重要！)
    logger.exception(f"Uncaught Exception: {str(exc)} - URL: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": 500, "message": "服务器内部错误，请联系管理员", "data": None},
    )