from typing import Union
from decimal import Decimal
from eth_utils import to_wei, from_wei


unit_denominations = {
    'wei': 10 ** -18,
    'kwei': 10 ** -15,
    'mwei': 10 ** -12,
    'gwei': 10 ** -9,
    'szabo': 10 ** -6,
    'finney': 10 ** -3,
    'ether': 1,
    
}

class Unit:
    unit: str
    decimals: int
    Wei: int
    KWei: Decimal
    MWei: Decimal
    GWei: Decimal
    Szabo: Decimal
    Finney: Decimal
    Ether: Decimal
    def __init__(self, amount: Union[str, int, float, Decimal], unit: str):
        self.unit = unit
        self.decimals = 18
        self.Wei = to_wei(amount, self.unit)
        self.KWei = from_wei(self.Wei, 'kwei')
        self.MWei = from_wei(self.Wei, 'mwei')
        self.GWei = from_wei(self.Wei, 'gwei')
        self.Szabo = from_wei(self.Wei, 'szabo')
        self.Finney = from_wei(self.Wei, 'finney')
        self.Ether = from_wei(self.Wei, 'ether')
        

class Wei(Unit):
    def __init__(self):
        pass
    
class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = True) -> None:
        
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals