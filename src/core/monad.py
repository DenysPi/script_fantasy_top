import os
import base64
import hashlib
import asyncio


from src.db.models import Accounts
from src.data.session import BaseAsyncSession
from src.core.base import Base
class Fantasy(Base):
    def __init__(self, data:Accounts, session: BaseAsyncSession):
        super().__init__( data=data, async_session=session)
        self.version = self.data.user_agent.split('Chrome/')[1].split('.')[0]
        self.platform = self.data.user_agent.split(' ')[1][1:].replace(';', '')
        if self.platform == "Macintosh":
            self.platform = "MacOS"
        elif self.platform == "X11":
            self.platform = "Linux"
        self.code_verif = None
        
    @staticmethod
    def generate_state():
        return base64.urlsafe_b64encode(os.urandom(48)).decode("utf-8").rstrip("=")
    
    @staticmethod
    def generate_code_challenge():
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8").rstrip("=")
        sha256_hash = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(sha256_hash).decode("utf-8").rstrip("=")
        return code_verifier, code_challenge
        
    
    
        
    
    
fantasy = Fantasy(data= Accounts(
    eth_pk=1,
    evm_address='0x1234567890abcdef',
    proxy='192.168.1.1',
    email='test@example.com',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    ), session=BaseAsyncSession)

async def main():
    async with BaseAsyncSession(proxy=None) as session:  # Ensure it's instantiated
        fantasy = Fantasy(
            data=Accounts(
                eth_pk=1,
                evm_address='0x1234567890abcdef',
                proxy = '1',
                email='test@example.com',
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            ),
            session=session  # Pass the properly instantiated session
        )
        await fantasy.get_auth_google_link()

asyncio.run(main())

