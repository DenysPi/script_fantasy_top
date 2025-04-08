import os
from src.config.config import logger
try:
    ASYNC_TASK_IN_SAME_TIME: int = int(os.getenv('ASYNC_TASK_IN_SAME_TIME'))
    
except Exception:
    logger.warning('Вы не создали .env и не добавили туда настройки')