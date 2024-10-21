from fastapi import FastAPI
import uvicorn

# Create an instance of FastAPI
app = FastAPI()

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}

# Another route that takes a parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# POST route example
@app.post("/create_item/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

# If this file is the main module, run the FastAPI app using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
