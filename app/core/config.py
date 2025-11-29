import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    # 动态计算 .env 文件的绝对路径
    # __file__ 是当前文件 (config.py) 的路径
    # .parent.parent.parent 会回退到项目根目录 (cbeop-backend/)
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()