import sqlite3
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib


# conn = sqlite3.connect('./wallets.db', check_same_thread=False)
# c = conn.cursor()

# c.execute("select * from wallets where public_key = ?",('041dbd159a642ec400e99e992585de03622da20151cb07dd78549566e5610555c6ba9d13818ab85f400d3f2a7674b8e4409273f2bd441c58862643230b7733a5e3',))
# print(c.fetchall())


# private_key_testing = '1170f1d9b8df97e17ece686e4ce7155c66650a306a4a0dfb092f11e5e0bac1c4'
# 04addd391c53de0eba0aac9e2400c65b90420b084bd01c70fa7bbaded42e2f749012165a486690a19901931f3a80c4838b91cc500e9394de7f0ea018c128acaf60


# private_key = SigningKey.generate(curve=SECP256k1)
# public_key = private_key.get_verifying_key()

# message = "Send 10 coins to Bob"
# # Hash the message using SHA-256
# message_hash = hashlib.sha256(message.encode('utf-8')).digest()

# # 3. Sign the message hash with the private key
# signature = private_key.sign(message_hash)

# # 4. Verify the signature with the public key
# try:
#     valid = public_key.verify(signature, message_hash)
#     print("Signature is valid:", valid)
# except:
#     print("Signature verification failed.")


# sender 1170f1d9b8df97e17ece686e4ce7155c66650a306a4a0dfb092f11e5e0bac1c4
# 04d3660917e9d912968d529928c652c7023e7a12887eb63dc236fa0065265a7d807726df09beb9a1d23cc42d3eead8a808adea729fefea50d3c7a702f466314da4


# 041dbd159a642ec400e99e992585de03622da20151cb07dd78549566e5610555c6ba9d13818ab85f400d3f2a7674b8e4409273f2bd441c58862643230b7733a5e3
# 7fca3fb86280f346b2c4ed6b0d7d069e6f81902787033d8239a49b3681137ea9


# MAKING a NFT

conn = sqlite3.connect('./assets.db', check_same_thread=False)
c = conn.cursor()

c.execute(""" 
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_info TEXT,
    hash TEXT UNIQUE,
    added_by TEXT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")

# asset_info = {"type":"house", "address":"123xyzstreet","pincode":"120210","area":"100x50x50"}
# string = f'{asset_info}'
# hash_obj = hashlib.sha256()
# hash_obj.update(string.encode())
# hash = hash_obj.hexdigest()
# print(hash)
# # c.execute('insert into assets (asset_info,hash,added_by) values(?,?,?)',(str(asset_info),hash,'Vansh'))
# # conn.commit()
# c.execute("select * from assets")
# print(c.fetchall())

def create_NFT(asset_info:dict):
    hash_obj = hashlib.sha256()
    hash_obj.update(str(asset_info).encode())
    hash = hash_obj.hexdigest()
    return hash

def add_NFT_to_DB(asset_info:dict,hash:str,added_by:str):
    c.execute('INSERT INTO assets (asset_info,hash,added_by) VALUES(?,?,?)',(str(asset_info),hash,added_by))
    conn.commit()
    return True

# 04e330bd8c55132508e4e782376784bc90ab877449c1d93ca9f25276f84ec2d15f0969e9777fb14718971c578a5267f0c949848811b7c186d2c76d0cb15cf75cdd
# 043201c77831f5a4ff5052a728aa7b9677bbda14ad4c2fc50901f211dff88f807f5409e2dd060f33db5f9c5a2fc9322b5beb7b05be93f1bbbf5793ecdd4a9b2184

# 740769cd47d4812a9ac5d2df268f3e5c9f595c799cca078cb8b07871309947ed
# 08137ce2d2fd200459f866ad1cb320fc3b5ddf4166d4fbb376376ba0c38c0d33

print(create_NFT('genesis block'))