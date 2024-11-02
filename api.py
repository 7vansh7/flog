from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import sys 
from pydantic import BaseModel
sys.path.append('./')
from wallet_db import create_user,get_user_holdings,add_user_holdings, get_all_public_keys


app = FastAPI()

# replace the get methods with the post methods
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Wallet_info_model(BaseModel):
    private_key: str

class Wallet_add_model(BaseModel):
    private_key: str
    change: str

@app.get("/")
def read_root():
    return {"message": "Fuck you, this is a void"}

@app.post("/wallet_info/")
def wallet_info(Private_key: Wallet_info_model):
    holdings = get_user_holdings(Private_key.private_key)
    return {"message": holdings}

@app.get("/create_wallet/")
def create_new_wallet():
    private_key, public_key = create_user()
    return {"message":"wallet created successfully, please store these keys as they won't be shown again ",
             "private_key": private_key, "public_key": public_key}

@app.post("/wallet_add/")
def add_to_holdings(params:Wallet_add_model):
    add_user_holdings(params.private_key,params.change)
    return {"message":f"added {params.change}"}

@app.get("/all_public_keys")
def all_wallets_public_keys():
    keys = get_all_public_keys()
    return {"keys":keys}

if __name__ == "__main__":
    uvicorn.run('api:app', host="127.0.0.1", port=8000, reload=True)

