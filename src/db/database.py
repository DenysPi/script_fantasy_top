import asyncio

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
    
    
    async def add_account(self, eth_pk: int):
        async with AsyncSession(self.engine) as session:
            new_account = Accounts(
                            evm_pk= 123,
                            evm_address="0x1234567890abcdef",  # Example address
                            proxy="proxy_value",
                            email="user@example.com",
                            user_agent="Mozilla/5.0"
                        )
            session.add(new_account)
            await session.commit()
    


db = Database(
    db_url=f'sqlite+aiosqlite:///{config.ACCOUNTS_DB}',
    pool_recycle=3600,
    connect_args={'check_same_thread': False}
)
    
async def initialize_db():
    await db.create_table(Base)
    
    


# You can call test_root_dir() here or in your main() async function


# Example function to add an account

# Main function to initialize DB and interact with it
async def main():
    await initialize_db()
    print('Database Initialized')

    # Example of adding a new account
    await db.add_account("user1")
    print("Account added!")

    # Example of querying all accounts
    accounts = await db.get_all_accounts()
    print("Accounts:", accounts)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())