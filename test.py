import sqlite3

conn = sqlite3.connect('./wallets.db', check_same_thread=False)
c = conn.cursor()

c.execute("select * from wallets")
print(c.fetchall())