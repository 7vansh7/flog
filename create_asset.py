import sqlite3
import hashlib


conn = sqlite3.connect('./DB/assets.db', check_same_thread=False)
c = conn.cursor()

c.execute(""" 
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_info TEXT,
    hash TEXT UNIQUE,
    added_by TEXT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")

asset_info = {"type":"car", "name":"hyundai i10"}
asset_info = {"type":"house", "address":"2323,xyzstreet,delhi","pincode":110023,"area":"3000x12x121"}
asset_info = {"type":"painting", "name":"Mona Lisa"}
asset_info = {"type":"Watch", "name":"Rolex Daytona Rainbow"}
asset_info = {"type":"Airplane", "name":"Boeing 747"}
added_by = 'Vansh'

def create_NFT(asset_info:dict):
    hash_obj = hashlib.sha256()
    hash_obj.update(str(asset_info).encode())
    hash = hash_obj.hexdigest()
    return hash

def add_NFT_to_DB(asset_info:dict,hash:str,added_by:str):
    c.execute('INSERT INTO assets (asset_info,hash,added_by) VALUES(?,?,?)',(str(asset_info),hash,added_by))
    conn.commit()

# add_NFT_to_DB(asset_info, create_NFT(asset_info),added_by)

# c.execute("select * from assets")
# print(c.fetchall())