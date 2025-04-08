import asyncio

from src.config.config import config
from src.utils.reset_count_progress import set_progress_to_zero
from src.utils.user_menu import *

def main():
    
    while True:
        set_progress_to_zero()
        user_action = get_action()
        
        semaphore = asyncio.Semaphore(ASYNC_TASK_IN_SAME_TIME)
        
        match user_action:
            case 'Aircraft':
                asyncio.run(get_start(semaphore))
                        
    
main()