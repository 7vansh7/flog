import sqlite3
from wallet_db import get_public_key_from_private_key
import hashlib

GENESIS_BLOCK_HASH = '56360bfb8218a44dd9943b4f7ea8a4ef80109e067c9d9da3dc7605be50126abb'

# c.execute(""" 
# CREATE TABLE IF NOT EXISTS transactions (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     public_key_sender TEXT ,
#     public_key_receiver TEXT ,
#     change TEXT,
#     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# )""")

# c.execute(""" 
# CREATE TABLE IF NOT EXISTS blockchain (
#     block_no INTEGER PRIMARY KEY AUTOINCREMENT,
#     public_key_sender TEXT ,
#     public_key_receiver TEXT ,
#     change TEXT,
#     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     hash TEXT UNIQUE,
#     previous_hash TEXT
# )""")

def add_transaction_to_DB(private_key_sender, public_key_receiver, change):
    conn = sqlite3.connect('./DB/transactions.db', check_same_thread=False)
    c = conn.cursor()
    try:
        public_key_sender = get_public_key_from_private_key(private_key_sender)
        c.execute(""" INSERT INTO transactions (public_key_sender, public_key_receiver, change)
                VALUES (?,?,?)""",(public_key_sender,public_key_receiver,change))
        conn.commit()
        conn.close()
        add_block(public_key_sender, public_key_receiver, change)
        return {"message":"transaction successfully added"}
    except sqlite3.Error as e:
        print(e)
        conn.close()
        return e

def add_block(public_key_sender, public_key_receiver, change):
    conn = sqlite3.connect('./DB/transactions.db', check_same_thread=False)
    c = conn.cursor()
    previous_hash = c.execute('SELECT * FROM blockchain ORDER BY block_no DESC LIMIT 1').fetchone()[5]
    string = f'{public_key_sender},{public_key_receiver},{change},{previous_hash}'
    hash_obj = hashlib.sha256()
    hash_obj.update(string.encode())
    hash = hash_obj.hexdigest()
    c.execute("""INSERT INTO blockchain (public_key_sender,public_key_receiver,change,hash
              ,previous_hash) VALUES(?,?,?,?,?)""",(public_key_sender,
                                                    public_key_receiver,change,hash,previous_hash))
    conn.commit()
    conn.close()

def get_all_transactions():
        conn = sqlite3.connect('./DB/transactions.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM transactions")
        data = c.fetchall()
        conn.close()
        return data

# add_transaction_to_DB('1170f1d9b8df97e17ece686e4ce7155c66650a306a4a0dfb092f11e5e0bac1c4',
#                       '041dbd159a642ec400e99e992585de03622da20151cb07dd78549566e5610555c6ba9d13818ab85f400d3f2a7674b8e4409273f2bd441c58862643230b7733a5e3',
#                       'test transaction')


# conn.close()
# c.execute('Insert into blockchain (public_key_sender,public_key_receiver,change,hash,previous_hash) values(?,?,?,?,?)',(dash,dash,gen_block,key,dash,))
# conn.close()
# conn.commit()
# print(get_all_transactions())
# conn.close()
# conn = sqlite3.connect('./DB/transactions.db', check_same_thread=False)
# c = conn.cursor()
# print(c.execute('select * from blockchain').fetchall())
# dash = '-'
# key = '56360bfb8218a44dd9943b4f7ea8a4ef80109e067c9d9da3dc7605be50126abb'
# gen_block = 'genesis block'
# c2.execute('Insert into blockchain (public_key_sender,public_key_receiver,change,hash,previous_hash) values(?,?,?,?,?)',(dash,dash,gen_block,key,dash,))
# conn2.commit()
# conn.rollback()
# add_transaction_to_DB('740769cd47d4812a9ac5d2df268f3e5c9f595c799cca078cb8b07871309947ed',
#                       '043201c77831f5a4ff5052a728aa7b9677bbda14ad4c2fc50901f211dff88f807f5409e2dd060f33db5f9c5a2fc9322b5beb7b05be93f1bbbf5793ecdd4a9b2184',
#                       'f16fc966f4367feda8099ce9be824b7ac6526505d21b58fafc480933207263a8')
