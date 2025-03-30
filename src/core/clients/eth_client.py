import logging
import asyncio

from typing import Optional
from web3 import AsyncWeb3
from web3.eth import AsyncEth
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress

from src.utils.eth_convert import TokenAmount
from src.db.models import Accounts
from src.data.models import Network, Networks
from src.data.models import Wallet, Contracts, Transactions


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            'user-agent': user_agent or 'default-user-agent'  
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

    async def send_native(self, data: Accounts, amount: TokenAmount, address: Optional[ChecksumAddress] = None):
        balance = await self.w3.eth.get_balance(self.account.address)
        print(f"Balance: {balance}")
        
        # Calculate the nonce and fees
        nonce = await self.w3.eth.get_transaction_count(self.account.address)
        print(nonce)
        max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
        base_fee = (await self.w3.eth.fee_history(1, "latest"))["baseFeePerGas"][-1]
        max_fee_per_gas = base_fee + max_priority_fee_per_gas
        

        
        tx = {
            "type": self.network.tx_type,
            "chainId": self.network.chain_id,
            "nonce": nonce,
            "to": address,
            "value": amount.Wei,  
            "maxPriorityFeePerGas": max_priority_fee_per_gas,
            "maxFeePerGas": max_fee_per_gas,
            "gas": 21000,  
        }

        
        signed_txn = self.w3.eth.account.sign_transaction(tx, self.account._private_key)

        try:
           
            tx_hash = await self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            logger.info(f"[{data.id}] | {data.evm_address} | Transaction sent! Waiting for status...")

         
            receipt = await self.w3.eth.wait_for_transaction_receipt(tx_hash)

            if isinstance(receipt, dict):
   
                if 'status' in receipt:
                    if receipt['status'] == 1:
                        logger.info(f"Transaction successful: {tx_hash.hex()}")
                        return True, tx_hash.hex()
                    else:
                        logger.warning(f"Transaction failed: {tx_hash.hex()}")
                        return False, None
                else:
                
                    logger.warning(f"[{data.id}] | {data.evm_address} | Transaction failed | Hash: {self.network.explorer}{tx_hash.hex()}")
                    return False, None

        except Exception as e:
            logger.error(f"[{data.id}] | {data.evm_address} | Error during the transaction: {str(e)}")
            return False, None


# Example of test function to send a transaction
# async def test_send_monad():
#     private_key = ''
#     monad_client = ETHClient(private_key=private_key, network= Networks.Monad)

#     
#     data = Accounts(eth_pk=private_key, evm_address='0x2d7E7df4dc1403cc33696aFd0FdCbBdfDd15c5bC', proxy=None, email=None, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')  # Replace with actual data
#     amount = TokenAmount(1100000000000000000)  

#     
#     success, tx_hash = await monad_client.send_native(data, amount, address="0x2d7E7df4dc1403cc33696aFd0FdCbBdfDd15c5bC")
    
#     if success:
#         print(f"Transaction successful! Hash: {tx_hash}")
#     else:
#         print(f"Transaction failed.")


# asyncio.run(test_send_monad())

