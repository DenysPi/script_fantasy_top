import os
import base64
import hashlib

from src.db.models import Accounts
from src.data.session import BaseAsyncSession
from src.core.base import Base
class Fantasy(Base):
    def __init__(self, data:Accounts, session: BaseAsyncSession):
        super().__init__(data=data, async_session=session)
        self.version = self.data.user_agent.split('Chrome/')[1].split('.')[0]
        self.platform = self.data.user_agent.split(' ')[1][1:].replace(';', '')
        if self.platform == "Macintosh":
            self.platform = "MacOS"
        elif self.platform == "X11":
            self.platform = "Linux"
    @staticmethod
    def generate_state(self):
        return base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    
    @staticmethod
    def generate_code_challenge(self):
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8").rstrip("=")
        sha256_hash = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(sha256_hash).decode("utf-8").rstrip("=")
        return code_verifier, code_challenge
        
        
    def main_header(self):
        return {
            "method": "POST",
            "path": "/api/v1/oauth/init",
            "scheme": "https",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6",
            "content-length": "196",
            "content-type": "application/json",
            "origin": "https://monad.fantasy.top",
            "priority": "u=1, i",
            "privy-app-id": "cm6ezzy660297zgdk7t3glcz5",
            "privy-ca-id": "0a451521-e4fa-4dde-9dc1-cf0738993685",
            "privy-client": "react-auth:1.92.3",
            "privy-client-id": "client-WY5gEtuoV4UpG2Le3n5pt6QQD61Ztx62VDwtDCZeQc3sN",
            "referer": "https://monad.fantasy.top/",
            "sec-ch-ua": f'"Chromium";v="{self.version}", "Not:A-Brand";v="24", "Google Chrome";v="{self.version}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": f'{self.platform}',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-fetch-storage-access": "active",
            "user-agent": f'{self.data.user_agent}'
        }
    
    def aunt_via_google(self):
        headers = self.main_header()
        data = {
            'code_challenge': f'{self.generate_code_challenge(self)[1]}',
            'provider': "google",
            'redirect_to': "https://monad.fantasy.top/login",
            'state_code': f'{self.generate_state(self)}'
        }
        return data

        
    
    
fantasy = Fantasy(data= Accounts(
    eth_pk=1,
    evm_address='0x1234567890abcdef',
    proxy='192.168.1.1',
    email='test@example.com',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    ), session=BaseAsyncSession)

print(fantasy.aunt_via_google())