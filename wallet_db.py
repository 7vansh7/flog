import sqlite3
import os 
import ecdsa


# conn = sqlite3.connect('./DB/wallets.db', check_same_thread=False)
# c = conn.cursor()


# c.execute(""" 
# CREATE TABLE IF NOT EXISTS wallets (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     public_key TEXT UNIQUE,
#     private_key TEXT UNIQUE,
#     holdings TEXT,
#     timestamp TEXT
# )""")

def create_user():
    conn = sqlite3.connect('./DB/wallets.db', check_same_thread=False)
    c = conn.cursor()
    private_key = os.urandom(32)
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.verifying_key
    public_key = b'\04' + verifying_key.to_string()
    c.execute("INSERT INTO wallets (public_key, private_key) VALUES (?, ?)", (public_key.hex(), private_key.hex()))
    print(private_key.hex() ,"\n\n", public_key.hex())
    conn.commit()
    conn.close()
    return private_key.hex(),public_key.hex()

def get_user_holdings(private_key):
    conn = sqlite3.connect('./DB/wallets.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT holdings FROM wallets WHERE private_key = ?", (private_key,))
    holdings = c.fetchall()
    conn.close()
    return holdings

def add_user_holdings(public_key, change):      
        conn = sqlite3.connect('./DB/wallets.db', check_same_thread=False)
        c = conn.cursor() 
        c.execute("UPDATE wallets SET holdings = COALESCE(holdings, '') || ? WHERE public_key = ?", (f';{change}', public_key))
        conn.commit()
        conn.close()
     
def get_all_public_keys():
     conn = sqlite3.connect('./DB/wallets.db', check_same_thread=False)
     c = conn.cursor()
     keys = ''
     c.execute("SELECT * FROM wallets")
     data = c.fetchall()
     for d in data:
        keys += f'{d[1]},' 
     conn.close()
     return keys

def delete_from_wallet(private_key,change):
    conn = sqlite3.connect('./DB/wallets.db', check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute("""
                UPDATE wallets SET holdings = TRIM(REPLACE(holdings, ?, '')) 
                    WHERE private_key = ? AND holdings LIKE '%' || ? || '%';
                """,(change,private_key,change,))
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(e)
        conn.close()

def get_public_key_from_private_key(private_key):
     conn = sqlite3.connect('./DB/wallets.db', check_same_thread=False)
     c = conn.cursor()
     c.execute("SELECT public_key FROM wallets WHERE private_key = ?",(private_key,))
     public_key_sender = c.fetchone()[0]
     conn.close()
     return public_key_sender

# c.execute("SELECT public_key FROM wallets WHERE private_key = ?",('1170f1d9b8df97e17ece686e4ce7155c66650a306a4a0dfb092f11e5e0bac1c4',))
# print(c.fetchone()[0])

# key =get_public_key_from_private_key('7fca3fb86280f346b2c4ed6b0d7d069e6f81902787033d8239a49b3681137ea9',)
# print(key)

# key = '043201c77831f5a4ff5052a728aa7b9677bbda14ad4c2fc50901f211dff88f807f5409e2dd060f33db5f9c5a2fc9322b5beb7b05be93f1bbbf5793ecdd4a9b2184'
# c.execute('select * from wallets where public_key = ?;',(key,))
# print(c.fetchone())