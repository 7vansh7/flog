from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Fuck you, this is the home page"}

@app.get("/wallet_info/{Key}")
def wallet_info(Key: str):
    # add the logic to retrieve wallet info using public key from the DB
    return {"item_id": item_id, "query": q}

@app.post("/create_wallet/")
def create_new_wallet():
        # add the logic to create private and public key, also store the info in a DB
    return {"message":"wallet created successfully", "private_key":"","public_key":""}


if __name__ == "__main__":
    uvicorn.run('api:app', host="127.0.0.1", port=8000, reload=True)
