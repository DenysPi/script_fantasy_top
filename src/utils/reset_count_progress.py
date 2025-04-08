from src.config.config import config


def set_progress_to_zero():
    config.remaining_tasks[0] = 0
    config.completed_tasks[0] = 0