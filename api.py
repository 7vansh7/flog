from fastapi import FastAPI
import uvicorn
import sys 
sys.path.append('./')
from wallet_db import create_user,get_user_holdings,add_user_holdings

app = FastAPI()

# replace the get methods with the post methods

@app.get("/")
def read_root():
    return {"message": "Fuck you, this is a void"}

@app.get("/wallet_info/{Private_key}")
def wallet_info(Private_key: str):
    holdings = get_user_holdings(private_key=Private_key)[0][0]
    return {"message": holdings}

@app.get("/create_wallet/")
def create_new_wallet():
    private_key, public_key = create_user()
    return {"message":"wallet created successfully, please store these keys as they won't be shown again ",
             "private_key": private_key, "public_key": public_key}

@app.get("/wallet_add/{Private_key}/{Change}")
def add_to_holdings(Private_key,Change):
    add_user_holdings(Private_key,Change)
    return {"message":f"added {Change}"}

if __name__ == "__main__":
    uvicorn.run('api:app', host="127.0.0.1", port=8000, reload=True)

