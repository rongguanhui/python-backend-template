from celery import Celery
from app.core.config import settings
from celery.schedules import crontab

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "app.workers.tasks.generate_ai_content": "ai-queue", # 专门的队列处理AI
}

celery_app.conf.beat_schedule = {
    # 任务1: 每小时检查一次库存
    "check-stock-every-hour": {
        "task": "app.workers.tasks.check_low_stock",
        "schedule": crontab(minute=0, hour="*"), # 每小时第0分钟执行
    },
    # 任务2: 每天凌晨1点清理过期日志/临时文件
    "daily-cleanup": {
        "task": "app.workers.tasks.cleanup_temp_files",
        "schedule": crontab(minute=0, hour=1),
    },
    # 任务3: 每 30 秒测试一下 (开发调试用)
    "test-heartbeat": {
        "task": "app.workers.tasks.test_task",
        "schedule": 30.0, # 秒
        "args": (16, 16)
    }
}