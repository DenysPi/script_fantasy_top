import asyncio
from typing import List, Union

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from src.db.models import Base, Accounts
from src.config.config import config

class Database:
    def  __init__(self, db_url:str, **kwargs):
        self.db_url = db_url
        self.engine = create_async_engine(self.db_url, **kwargs)
        self.base = None
        
    async def create_table(self, base):
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)
            
    async def get_all_accounts(self):
        async with AsyncSession(self.engine) as session:
            query = select(Accounts)
            result = await session.execute(query)
            return result.scalars().all()
    
    
    async def add_account(self,row: Union[object, List[object]] ):
        async with AsyncSession(self.engine) as session:
            if isinstance(row, list):
                session.add_all(row)
            elif isinstance(row, object):
                session.add(row)
            else:
                raise DBException('Wrong type!')
            await session.commit()
            await session.commit()
    



