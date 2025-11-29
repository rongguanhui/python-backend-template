import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings

# 定义日志路径
LOG_PATH = Path("logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)

# 日志格式
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"


def setup_logging():
    # 1. 移除默认的 handler (避免重复输出)
    logger.remove()

    # 2. 输出到控制台 (Console)
    logger.add(
        sys.stderr,
        format=LOG_FORMAT,
        level="INFO",  # 生产环境可以改成 WARNING
        enqueue=True,
    )

    # 3. 输出到文件 (File) - 每天一个文件，保留 10 天
    logger.add(
        str(LOG_PATH / "app_{time:YYYY-MM-DD}.log"),
        rotation="00:00",  # 每天午夜切割
        retention="10 days",  # 只保留最近10天
        compression="zip",  # 历史日志压缩
        format=LOG_FORMAT,
        level="INFO",
        enqueue=True,
        encoding="utf-8"
    )

    return logger