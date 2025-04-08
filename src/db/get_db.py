from src.config.config import config
from src.db.database import Database
db = Database(
    db_url=f'sqlite+aiosqlite:///{config.ACCOUNTS_DB}',
    pool_recycle=3600,
    connect_args={'check_same_thread': False}
)


async def get_accounts(quest):
    pass