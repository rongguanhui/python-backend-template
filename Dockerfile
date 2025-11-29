FROM python:3.10-slim

WORKDIR /code

# 安装系统依赖 (编译 asyncpg 需要)
RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .