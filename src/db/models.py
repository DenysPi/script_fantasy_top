from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text, Boolean, DateTime


Base = declarative_base()


class Accounts(Base):
    __tablename__ = 'accounts'
    eth_pk = Column(Integer, primary_key=True)
    evm_address = Column(Text, unique=True)
    proxy = Column(Text)
    email = Column(Text)

    user_agent = Column(Text)
    finished = Column(Boolean)
    

    def __init__(
            self,
            evm_pk: str,
            evm_address: str,
            proxy: str,
            email: str,
            user_agent: str,
    ) -> None:
        
        self.evm_pk = evm_pk
        self.evm_address = evm_address
        self.proxy = proxy
        self.email = email

        self.user_agent = user_agent

        self.finished = False
    