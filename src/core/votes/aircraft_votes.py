
import asyncio
from web3 import Web3
from eth_account.messages import encode_defunct
from src.db.models import Accounts
from src.data.session import BaseAsyncSession
from src.core.clients.eth_client import ETHClient
from src.core.base import Base
from src.data.models import Networks, Contracts, DefaultABIs, TokenAmount

from src.config.config import logger


class Aircraft(Base):
    def __init__(self, data:Accounts, async_session:BaseAsyncSession, eth_client: ETHClient | None = None, network=Networks.Monad):
        super().__init__(data= data, async_session=async_session)
        self.version = self.data.user_agent.split('Chrome/')[1].split('.')[0]
        self.platform = self.data.user_agent.split(' ')[1][1:].replace(';', '')
        
        if self.platform == "Macintosh":
            self.platform = "MacOS"
        elif self.platform == "X11":
            self.platform = "Linux"
            
            
        if eth_client:
            self.eth_client = eth_client
        else:
            self.eth_client = ETHClient(
                private_key="", network=network, proxy=self.data.proxy, user_agent=self.data.user_agent
            )

        
    def main_header(self):
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            
            'content-type': 'application/json',
            'origin': 'https://aicraft.fun',
            'priority': 'u=1, i',
            'referer': 'https://aicraft.fun/',
            'sec-ch-ua': f'"Not_A(Brand";v="8", "Chromium";v="{self.version}", "Google Chrome";v="{self.version}"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': f'"{self.platform}"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.data.user_agent,
     
        }
        
    async def get_message_code(self):
        json_data = {
            "address": self.data.evm_address,
            "type": "ETHEREUM_BASED"
        }
        response = await self.async_session.get(
            f"https://api.aicraft.fun/auths/wallets/sign-in/message?address={self.data.evm_address}&type=ETHEREUM_BASED",
            headers=self.main_header(),
            json=json_data
        )
        if response.status_code == 200:
            return True, response.json().get('data')['message']
        else:
            logger.error(f"[{self.data.id}] | {self.data.evm_address} can't receive a message from AirCraft")
            
            
    async def get_authefication_token(self, message):
        
        
        message = (
            f"{message}"
        )
        message_encoded = encode_defunct(text=message)
        
        signed_message = self.eth_client.account.sign_message(message_encoded)
        
        
        signature_hex = signed_message.signature.hex()
       
        json_data = {
            "address": self.data.evm_address.lower(),
            "message": message,
            "signature": "0x"+signature_hex,  # Correct signature format
            "type": "ETHEREUM_BASED"
        }
       
        
        response = await self.async_session.post(
            'https://api.aicraft.fun/auths/wallets/sign-in', 
            headers=self.main_header(), 
            json=json_data
        )
        
        if response.status_code == 201:
            auntefication_token = response.json().get('data').get('token')
            return True, auntefication_token
        logger.error(f'[{self.data.id}] | {self.data.evm_address} not permited')
        return False, response.json()
        
        
    async def get_profile_info(self, auth_token):
        headers = self.main_header()
        headers["authorization"] = f'Bearer {auth_token}'
        
        response = await self.async_session.get(
            'https://api.aicraft.fun/users/me?includePresalePurchasedAmount=true',
            headers=headers
        )
        
        if response.status_code == 200:
            json_data = response.json()
    
            id_profile = json_data.get('data', {}).get('wallets')[0].get('_id')
            id_refferal = json_data.get('data', {}).get('invitedBy').get('refCode')
            return True, (id_profile,id_refferal)
        
        logger.error(f"[{self.data.id}] | {self.data.evm_address} couldn't get profile info")
        return False, None
    
    
    async def get_candidates(self, auth_token):
        headers = self.main_header()
        headers["authorization"] = f'Bearer {auth_token}'
        
        response = await self.async_session.get(
            'https://api.aicraft.fun/candidates?projectID=678376133438e102d6ff5c6e',
            headers=headers
            
        )
        if response.status_code == 200:
            return True, response.json().get('data')
        logger.error(f"[self.data.id] | {self.data.evm_address} couldn't get candidates info")
    
    
    
    
    async def sorted_candidates(self, auth_token):
        status, candidates = await self.get_candidates(auth_token=auth_token)
        if status:
            
            dict_candidates = {}
            for candidate in candidates:
                canditate_country_code = candidate.get('metadata').get('countryCode')
                candidate_category_id = candidate.get('_id')
                
                if canditate_country_code and candidate_category_id:
                    dict_candidates[canditate_country_code] = candidate_category_id
            return True, dict_candidates
                
            
            
    
    async def get_transaction_info(self, auth_token):
        
        headers = self.main_header()
        headers["authorization"] = f'Bearer {auth_token}'
                
        status_info, profile_info = await self.get_profile_info(auth_token=auth_token)
        
        status_candidates, candidates = await self.sorted_candidates(auth_token=auth_token)
                
        if status_info and status_candidates:
            json_data = {
                "candidateID": candidates["UA"],
                "chainID": "10143",
                "feedAmount": 1,
                "refCode": profile_info[1],
                "walletID": profile_info[0]
                }
                
                
            response = await self.async_session.post(
                'https://api.aicraft.fun/feeds/orders',
                headers=headers,
                json= json_data
                )
                    
            if response.status_code == 201:
               
                return True, response.json()
            

            logger.error(f"[self.data.id] | {self.data.evm_address} sending of transaction was impossible")
                    
        logger.error(f"[self.data.id] | {self.data.evm_address} couldn't get info to make transaction")
                
                
    async def send_feed_transaction(self, auth_token):
        status, transaction = await self.get_transaction_info(auth_token)
        
        transaction_id = transaction.get('data').get("order").get("_id")
        
        abi = DefaultABIs()
        if status:
            contract_address = transaction.get('data').get('payment').get('contractAddress')
            checksummed_address = Web3.to_checksum_address(contract_address)
           
            params = transaction.get('data').get('payment').get('params')
        
            
            
            message_encoded = encode_defunct(hexstr=params['userHashedMessage']) 
        
            
        
            signed_message = self.eth_client.account.sign_message(message_encoded)
            signature_hex =signed_message.signature.hex()
            

       
            contract = await self.eth_client.contracts.get_contact(contract_address = checksummed_address, abi=abi.FeedContract)
        
            
            
            tx_func = contract.functions.feed(
                params['candidateID'],
                int(params['feedAmount']),
                params['requestID'],
                params['requestData'],
                bytes.fromhex(signature_hex),
                bytes.fromhex(params['integritySignature'][2:])
            )
            
            
            
           
            estimated_gas = await tx_func.estimate_gas({'from': self.data.evm_address})

     
            max_priority_fee_per_gas = await self.eth_client.w3.eth.max_priority_fee
            base_fee = (await self.eth_client.w3.eth.fee_history(1, "latest"))["baseFeePerGas"][-1]

       
            max_fee_per_gas = base_fee + max_priority_fee_per_gas
        
           
            

            
            transaction_data = {
                'from': self.data.evm_address,
                'to': checksummed_address,
                'gas': estimated_gas,
                'maxPriorityFeePerGas': max_priority_fee_per_gas,
                'maxFeePerGas': max_fee_per_gas,
                'chainId': 10143,
                'nonce': await self.eth_client.w3.eth.get_transaction_count(self.data.evm_address),
                'data': (await tx_func.build_transaction({'from': self.data.evm_address}))['data'] 
            }
            signed_transaction = self.eth_client.w3.eth.account.sign_transaction(transaction_data, private_key=self.data.eth_pk)
           
            
        
            tx_hash = await self.eth_client.w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
            tx_hash_hex = tx_hash.hex()
            
            return True, tx_hash_hex, transaction_id
        logger.error('bad request')
                
            
    
            
    async def confirm_daily_vote(self):
        status, message = await self.get_message_code()
        if not status:
            return

        status, auth_token = await self.get_authefication_token(message=message)
        if not status:
            return

        
        status_profile, profile_info = await self.get_profile_info(auth_token=auth_token)
       
        if not status_profile:
            return

        # Save refCode
        ref_code = profile_info[1]

        # Send transaction
        status, transaction_hash, id_transaction = await self.send_feed_transaction(auth_token=auth_token)
        if not status:
            return

        
        await asyncio.sleep(5)
        
        headers = self.main_header()
        headers["authorization"] = f'Bearer {auth_token}'
        
        
    
        json_data = {
            "refCode": ref_code,
            "transactionHash": "0x" + transaction_hash  
        }
        
        response = await self.async_session.post(
            f"https://api.aicraft.fun/feeds/orders/{id_transaction}/confirm",
            headers=headers,
            json=json_data
        )
        return response.json()
       
            
async def main():
    async with BaseAsyncSession(proxy=None) as session:  # Ensure it's instantiated
        aircraft = Aircraft(
            data=Accounts(
                eth_pk="",
                
                evm_address='0x6BdD89d8d575Ef5E6D3279FA667F580c13C27715',
                proxy = None,
                email='test@example.com',
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            ),
            async_session=session  
        )
        
        
        
        print(await aircraft.confirm_daily_vote())
        
       
asyncio.run(main())