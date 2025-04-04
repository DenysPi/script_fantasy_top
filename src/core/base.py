from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Accounts, db
from src.data.session import BaseAsyncSession


class Base:
    def __init__(self, data: Accounts, async_session: BaseAsyncSession):
        self.data = data
        if async_session:
            self.async_session = async_session
        else:
            BaseAsyncSession(
                proxy=self.data.proxy,
                user_agent=self.data.user_agent
            )
        self.version = self.data.user_agent.split('Chrome/')[1].split('.')[0]
        self.platform = self.data.user_agent.split(' ')[1][1:].replace(';', '')
        if self.platform == "Macintosh":
            self.platform = "MacOS"
        elif self.platform == "X11":
            self.platform = "Linux"
        
    async def write_to_db(self):
        async with AsyncSession(db.engine) as session:
            await session.merge(self.data)
            await session.commit()