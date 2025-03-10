from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import sys 
sys.path.append('./')
from wallet_db import create_user,get_user_holdings,add_user_holdings, get_all_public_keys, delete_from_wallet
from transactions_db import add_transaction_to_DB,get_all_transactions
from api_models import *


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    add_user_holdings(params.public_key,params.change)
    return {"message":f"added {params.change}"}

@app.get("/all_public_keys")
def all_wallets_public_keys():
    keys = get_all_public_keys()
    return {"keys":keys}

@app.post("/make_transaction/")
def make_transaction(data: Transaction_model):
    private_key = data.private_key
    receiver_public_key = data.receiver_public_key
    change = data.change
    sender_holdings = get_user_holdings(private_key)[0][0]
    if change in sender_holdings:
        delete_from_wallet(private_key,change)
        add_user_holdings(receiver_public_key,change)
        add_transaction_to_DB(private_key,receiver_public_key,change)
        return {"message":"Transaction made successfully"}
    else:
        return {"message":"There is an error"}

@app.get("/get_transactions/")
def get_transactions():
    transactions_array = get_all_transactions()
    data = ''
    for x in transactions_array:
        public_key_sender = x[1]
        public_key_receiver = x[2]
        pair = f'{public_key_sender},{public_key_receiver};'
        data += pair
    return {"data":data}

if __name__ == "__main__":
    uvicorn.run('api:app', host="127.0.0.1", port=8000, reload=True)

