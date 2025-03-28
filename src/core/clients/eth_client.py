from typing import Optional
from web3 import AsyncWeb3
from web3.eth import AsyncEth
from eth_account.signers.local import LocalAccount
from data.models import Network, Networks
from data.models import Wallet, Contracts, Transactions
class ETHClient:
    network: Network
    account: Optional[LocalAccount]
    w3: AsyncWeb3
    
    def __init__(
            self, 
            private_key: Optional[str] = None, 
            network: Network = Networks.Ethereum,
            proxy: Optional[str] = None, 
            user_agent: Optional[str] = None,
        ) -> None:
        
        self.network = network
        self.private_key: Optional[str] = private_key
        
        self.proxy: Optional[str] = proxy
        self.headers: dict = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': user_agent
        }
        
        self.w3 = AsyncWeb3(
            provider=AsyncWeb3.AsyncHTTPProvider(
                endpoint_uri=self.network.rpc,
                request_kwargs={'proxy': self.proxy, 'headers': self.headers}
            ),
            modules={'eth': (AsyncEth,)},
            middleware=[]
        )
        
        if private_key:
            self.account = self.w3.eth.account.from_key(private_key=private_key)

        self.wallet = Wallet(self)
        self.contracts = Contracts(self)
        self.transactions = Transactions(self)
