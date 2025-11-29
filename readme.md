# 🚀 FastAPI Enterprise SaaS Starter

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Build your next SaaS product in days, not months.**

这是一个现代化的、基于 Python 的后端脚手架，专为构建**跨境电商平台**、**企业级 SaaS** 或 **AI 应用**而设计。它集成了异步高性能架构、后台任务队列、多租户权限管理以及常见的 SaaS 业务模块（支付、邮件、审计、Excel 处理）。

不再重复造轮子，专注于你的核心业务逻辑。

---

## ✨ 核心特性 (Features)

### 🏗 架构与性能
*   **高性能异步内核**: 基于 `FastAPI` + `Uvicorn` + `AsyncPG`，全链路异步 IO，轻松应对高并发。
*   **ORM 2.0**: 使用 `SQLAlchemy 2.0` (Async) + `Alembic`，现代化的数据库操作与版本迁移。
*   **任务队列**: 内置 `Celery` + `Redis`，支持异步任务（如 AI 生成、发送邮件）和 **Cron 定时任务**。
*   **缓存加速**: 集成 `FastAPI-Cache2`，支持 Redis 缓存装饰器，大幅降低 DB 压力。

### 🔐 安全与权限
*   **企业级认证**: 完整的 JWT 身份认证（登录/注册/刷新）。
*   **RBAC 权限**: 基于角色的访问控制，支持超级管理员与普通用户。
*   **多租户隔离**: 数据层面的逻辑隔离，确保用户只能访问自己的资源。
*   **安全防护**: 内置 CORS、Rate Limiting (限流)、密码强哈希 (Bcrypt/Argon2)。

### 📦 开箱即用的业务模块
*   **💰 支付集成**: Stripe Webhook 对接示例，处理订阅与 VIP 状态更新。
*   **📧 邮件服务**: 异步邮件发送模块（验证码、通知）。
*   **📊 Excel 引擎**: 使用 Pandas/OpenPyXL 实现大批量数据的导入与导出。
*   **📝 审计日志**: 自动记录关键操作（谁、在什么时候、修改了什么）。
*   **🗑 软删除**: 防止数据误删，支持数据恢复。
*   **☁️ 对象存储**: S3/OSS 文件上传接口封装（代码模版）。
*   **🚩 功能开关**: Feature Flags 灰度发布支持。

### 🛠 工程化实践
*   **Docker Compose**: 一键启动 Web、DB、Redis、Worker、Beat。
*   **Pytest**: 集成 `pytest-asyncio`，提供 API 与 业务逻辑的自动化测试范例。
*   **Loguru**: 美观且强大的结构化日志系统，支持自动轮转。

---

## 🛠 技术栈 (Tech Stack)

| 模块 | 技术选型 |
| :--- | :--- |
| **Web Framework** | FastAPI |
| **Language** | Python 3.9+ |
| **Database** | PostgreSQL 15 |
| **ORM** | SQLAlchemy 2.0 (Async) |
| **Async Task** | Celery + Redis |
| **Validation** | Pydantic V2 |
| **Migration** | Alembic |
| **Testing** | Pytest |
| **Container** | Docker |

---

## 🚀 快速开始 (Quick Start)

### 方式一：Docker 一键启动 (推荐)

1.  **使用此模板**
    点击右上角的 `Use this template` 按钮，或 Clone 项目。

2.  **配置环境变量**
    ```bash
    cp .env.example .env
    # 编辑 .env 文件，修改数据库密码、Secret Key 等
    ```

3.  **启动服务**
    ```bash
    docker-compose up --build
    ```
    等待几秒后，访问：
    *   Swagger 文档: `http://localhost:8000/docs`
    *   Adminer (DB GUI): `http://localhost:8080` (如果在 docker-compose 中配置了)

---

### 方式二：本地开发

1.  **创建虚拟环境**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```

2.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

3.  **启动基础设施 (DB & Redis)**
    建议使用 Docker 启动基础设施，本地跑代码：
    ```bash
    docker-compose up -d db redis
    ```

4.  **数据库迁移**
    ```bash
    alembic upgrade head
    ```

5.  **启动服务**
    ```bash
    # 启动 API
    uvicorn app.main:app --reload

    # 启动 Worker (另开终端)
    celery -A app.workers.celery_app worker --loglevel=info

    # 启动 定时任务 Beat (另开终端)
    celery -A app.workers.celery_app beat --loglevel=info
    ```

---

## 📂 项目结构 (Project Structure)

```text
├── app/
│   ├── api/                 # API 路由 (Endpoints & Deps)
│   ├── core/                # 核心配置 (Config, Security, Logger)
│   ├── db/                  # 数据库连接与 Base 类
│   ├── models/              # SQLAlchemy 模型 (User, Product, Audit...)
│   ├── schemas/             # Pydantic 模型 (Request/Response)
│   ├── services/            # 业务逻辑层 (Email, Stripe, Excel...)
│   ├── workers/             # Celery 任务与定时配置
│   └── main.py              # FastAPI 入口
├── alembic/                 # 迁移脚本
├── tests/                   # 测试用例
├── .env.example             # 环境变量模版
├── docker-compose.yml       # 容器编排
└── requirements.txt         # 依赖列表