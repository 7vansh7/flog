from pydantic import BaseModel

class Wallet_info_model(BaseModel):
    private_key: str

class Wallet_add_model(BaseModel):
    public_key: str
    change: str

class Transaction_model(BaseModel):
    private_key: str
    change: str
    receiver_public_key: str