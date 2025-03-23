from typing import Optional

class Network:
    def  __init__(self, name:str, rpc:str, chain_id: Optional[int] = None, 
                tx_type:int=0,coin_symbol:Optional[str] = None,explorer: Optional[str]=None):
        self.name: str = name.lower()
        self.rpc: str = rpc
        self.chain_id: Optional[int] = chain_id
        self.tx_type: int = tx_type
        self.coin_symbol: Optional[str] = coin_symbol
        self.explorer: Optional[str] = explorer
        if self.coin_symbol:
            self.coin_symbol = self.coin_symbol.upper()
            
    
class Networks:
    Ethereum = Network(
        name='Ethereum',
        rpc='https://rpc.ankr.com/eth/',
        chain_id=1,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://etherscan.io/tx/',
    )
    
    