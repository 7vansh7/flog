from fastapi import FastAPI
import uvicorn
import sys 
sys.path.append('./')
from .wallet_db import get_data,add_data

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Fuck you, this is void"}

@app.get("/wallet_info/{Key}")
def wallet_info(Key: str):
    # add the logic to retrieve wallet info using public key from the DB
    return {"message":"your holdings are - "}

@app.post("/create_wallet/")
def create_new_wallet():
        # add the logic to create private and public key, also store the info in a DB
    return {"message":"wallet created successfully", "private_key":"","public_key":""}


if __name__ == "__main__":
    uvicorn.run('api:app', host="127.0.0.1", port=8000, reload=True)
