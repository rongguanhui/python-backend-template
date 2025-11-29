import time
from app.workers.celery_app import celery_app


@celery_app.task(name="generate_ai_content")
def generate_ai_content_task(product_id: int, product_title: str):
    """
    模拟一个耗时的 AI 生成任务
    真实场景：调用 OpenAI API 生成文案，然后调用 Stable Diffusion 生成图片
    """
    print(f"Start AI generation for Product ID: {product_id}...")

    # 模拟耗时 5 秒 (如果不使用 Celery，前端就会卡住 5 秒)
    time.sleep(5)

    # TODO: 这里应该连接数据库，更新该产品的 description 字段
    result = f"AI Optimized Description for {product_title}: Amazing quality..."

    print(f"Finished AI generation for {product_id}")
    return result

@celery_app.task(name="app.workers.tasks.check_low_stock")
def check_low_stock():
    # 注意：这里不能直接用 async 的 db session，需要用同步的方式，
    # 或者用 asgiref.sync.async_to_sync 包装
    # 为了简单，通常建议这里只做计算或调用外部 API，
    # 如果必须查库，建议在该 task 内部单独创建一个同步的 Session
    print("正在扫描库存不足的商品...")
    # ... 发邮件逻辑 ...
    return "Stock Checked"

@celery_app.task(name="app.workers.tasks.cleanup_temp_files")
def cleanup_temp_files():
    print("Daily Cleanup...")
    return "Daily Cleanup"

@celery_app.task(name="app.workers.tasks.test_task")
def test_task(product_id: int):
    print("Checking test_task...")
    return "test_task"
