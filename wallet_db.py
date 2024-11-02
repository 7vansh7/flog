import sqlite3
import hashlib
import os 
import ecdsa


conn = sqlite3.connect('./wallets.db', check_same_thread=False)
c = conn.cursor()


c.execute(""" 
CREATE TABLE IF NOT EXISTS wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    public_key TEXT UNIQUE,
    private_key TEXT UNIQUE,
    holdings TEXT,
    timestamp TEXT
)""")

def create_user():
    private_key = os.urandom(32)
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.verifying_key
    public_key = b'\04' + verifying_key.to_string()
    c.execute("INSERT INTO wallets (public_key, private_key) VALUES (?, ?)", (public_key.hex(), private_key.hex()))
    print(private_key.hex() ,"\n\n", public_key.hex())
    conn.commit()
    return private_key.hex(),public_key.hex()

def get_user_holdings(private_key):

    c.execute("SELECT holdings FROM wallets WHERE private_key = ?", (private_key,))
    holdings = c.fetchall()
    return holdings

def add_user_holdings(private_key, change):
           
	c.execute("""UPDATE wallets SET holdings = COALESCE(holdings, '') || ? WHERE private_key = ?""", (change, private_key))
	conn.commit()
     
def get_all_public_keys():
     keys = ''
     c.execute("SELECT * FROM wallets")
     data = c.fetchall()
     for d in data:
        keys += f'{d[1]},'
     return keys


# priv, pub = create_user()
# add_user_holdings('3c7871139c08108affca26f46664d915299ebafc64c2667801c66393fb1e9fc6',"car")
# holdings = get_user_holdings(private_key='3c7871139c08108affca26f46664d915299ebafc64c2667801c66393fb1e9fc6')
# print(holdings[0][0])

# c.execute("SELECT * FROM wallets WHERE private_key = ?", (priv,))
# print(c.fetchall())

# 3c7871139c08108affca26f46664d915299ebafc64c2667801c66393fb1e9fc6 

#  04d8205ebf5aa6edbec154fe364cb3f91ec3ae521a27d8447f14853d75db0af4eb974a5b06cce25048a5f41dc4dda5e2e7d6135294fb0bbfaea1b8e42ad5a25546


data = get_all_public_keys()
