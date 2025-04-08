from pathlib import Path
import sys
import os
import asyncio
from loguru import logger

class Config:
    def __init__(self):
        
        self.DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        
        
        if getattr(sys, 'frozen', False):
            self.ROOT_DIR = Path(sys.executable).parent.absolute()
        else:
            self.ROOT_DIR = Path(__file__).parent.parent.absolute()
            
        self.STATUS_DIR = os.path.join(self.ROOT_DIR, 'status')
        self.LOG = os.path.join(self.STATUS_DIR, 'log.txt')
        self.ACCOUNTS_DB = os.path.join(self.STATUS_DIR, 'accounts.db')
        
        
        
        
        
        self.completed_tasks = [0]
        self.remaining_tasks = [0]
        self.tasks_lock = asyncio.Semaphore(1)

        logger.add(self.LOG, format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}', level='DEBUG')
        
config = Config()

