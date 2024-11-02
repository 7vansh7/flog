from pydantic import BaseModel

class Wallet_info_model(BaseModel):
    private_key: str

class Wallet_add_model(BaseModel):
    private_key: str
    change: str

class Transaction_model(BaseModel):
    private_key: str
    change: str
    senders_public_key: str