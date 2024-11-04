import sqlite3
from wallet_db import get_public_key_from_private_key

conn = sqlite3.connect('./transactions.db', check_same_thread=False)
c = conn.cursor()

c.execute(""" 
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    public_key_sender TEXT ,
    public_key_receiver TEXT ,
    change TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")

def add_transaction_to_DB(private_key_sender, public_key_receiver, change):
    try:
        public_key_sender = get_public_key_from_private_key(private_key_sender)
        c.execute(""" INSERT INTO transactions (public_key_sender, public_key_receiver, change)
                VALUES (?,?,?)""",(public_key_sender,public_key_receiver,change))
        conn.commit()
        return {"message":"transaction successfully added"}
    except sqlite3.Error as e:
        print(e)
        return e
    
def get_all_transactions():
    c.execute("SELECT * FROM transactions")
    return c.fetchall()
