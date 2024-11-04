import sqlite3
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

def add_user_holdings(public_key, change):
           
	c.execute("""UPDATE wallets SET holdings = COALESCE(holdings, '') || ? WHERE public_key = ?""", (change, public_key))
	conn.commit()
     
def get_all_public_keys():
     keys = ''
     c.execute("SELECT * FROM wallets")
     data = c.fetchall()
     for d in data:
        keys += f'{d[1]},'
     return keys

def delete_from_wallet(private_key,change):
    try:
        c.execute("""
                UPDATE wallets SET holdings = TRIM(REPLACE(holdings, ?, '')) 
                    WHERE private_key = ? AND holdings LIKE '%' || ? || '%';
                """,(change,private_key,change,))
        conn.commit()

    except sqlite3.Error as e:
        print(e)

def get_public_key_from_private_key(private_key):
     c.execute("SELECT public_key FROM wallets WHERE private_key = ?",(private_key,))
     public_key_sender = c.fetchone()[0]
     return public_key_sender


# c.execute("SELECT public_key FROM wallets WHERE private_key = ?",('1170f1d9b8df97e17ece686e4ce7155c66650a306a4a0dfb092f11e5e0bac1c4',))
# print(c.fetchone()[0])

# key =get_public_key_from_private_key('7fca3fb86280f346b2c4ed6b0d7d069e6f81902787033d8239a49b3681137ea9',)
# print(key)