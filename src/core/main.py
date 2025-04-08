from src.db.models import Accounts

def get_start(semaphore, quest: str):
    if isinstance(quest, str):
        accounts: list[Accounts] = await get_accounts(quest)
    else:
        accounts: list[dict] = quest
        
        
def get_accounts(quest):
    pass

        

