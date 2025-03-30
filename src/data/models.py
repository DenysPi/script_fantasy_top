import asyncio
import logger
from typing import Optional, Union
from dataclasses import dataclass


from web3 import Web3
from eth_typing import ChecksumAddress
from web3.contract import AsyncContract

from src.utils.eth_convert import Wei, TokenAmount

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
    # Mainnets
    Ethereum = Network(
        name='Ethereum',
        rpc='https://rpc.ankr.com/eth/',
        chain_id=1,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://etherscan.io/tx/',
    )

    Arbitrum = Network(
        name='Arbitrum',
        rpc='https://rpc.ankr.com/arbitrum/',
        chain_id=42161,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://arbiscan.io/tx/',
    )

    Optimism = Network(
        name='Optimism',
        rpc='https://rpc.ankr.com/optimism/',
        chain_id=10,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://optimistic.etherscan.io/tx/',
    )

    Base = Network(
        name='Base',
        rpc='https://base-rpc.publicnode.com/',
        chain_id=8453,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://basescan.org/',
    )

    # Testnets
    Monad = Network(
        name='Monad Testnet',
        rpc= 'https://testnet-rpc.monad.xyz/',
        chain_id=10143,
        tx_type=2,
        coin_symbol='MON',
        explorer='https://testnet.monadexplorer.com/'
    )
    
@dataclass
class DefaultABIs:
    Token = [{
            'constant': True,
            'inputs': [],
            'name': 'name',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'symbol',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'totalSupply',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'decimals',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': 'who', 'type': 'address'}],
            'name': 'balanceOf',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': '_owner', 'type': 'address'}, {'name': '_spender', 'type': 'address'}],
            'name': 'allowance',
            'outputs': [{'name': 'remaining', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_spender', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': 'approve',
            'outputs': [],
            'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': 'transfer',
            'outputs': [], 'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        }]
    
    
class Wallet:
    def __init__(self, client):
        self.client = client
    async def balance(self, token_address: Optional[str] | None,
                      address: Optional[str] | None):
        if not address:
            address = self.client.account.address
        address = Web3.to_checksum_address(address)
        
        if not token_address:
            return Wei(await self.client.w3.eth.geget_balance(account=address))
        
        token_address = Web3.to_checksum_address(token_address)
        contract = self.client.contracts.get_contract(contract_address = token_address)
        return TokenAmount(
            amount= await contract.functions.balanceOf(address).call(),
            decimals=await contract.functions.decimals().call(),
            wei=True
            )
    
    async def nonce(self, address: Optional[ChecksumAddress] = None) -> int:
        if not address:
            address = self.client.account.address
        return await self.client.w3.eth.get_transaction_count(address)
        
class Contracts:
    def __init__(self, client) -> None:
        self.client = client
        
    async def get_contact(self,
                          contract_address: ChecksumAddress,
                          abi: Union[list, dict] = DefaultABIs
                          ) -> AsyncContract:
        return self.client.w3.eth.client(address = contract_address, abi=abi)
    


class Transactions:
    def __init__(self, client):
        self.client = client
        
    @staticmethod
    async def gaz_price(self, w3: Web3, max_retries= 20):
        retries = 0
        while retries < max_retries:
            try:
                return Wei(await w3.eth.gas_price)
            except asyncio.exceptions.TimeoutError:
                logger.debug(f"Retry {retries + 1}/{max_retries} due to TimeoutError ETH gas price")
                retries += 1

        raise ValueError(f"Unable to get gas price after {max_retries} retries")