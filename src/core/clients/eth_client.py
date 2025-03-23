from typing import Optional
from web3 import AsyncWeb3
from eth_account.signers.local import LocalAccount
from data.models import Network, Networks
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
        
        pass
        