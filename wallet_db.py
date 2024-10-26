import sqlite3
import hashlib


conn = sqlite3.connect('./walletDB')
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER UNIQUE AUTOINCREMENT,
                public_key TEXT UNIQUE,
                private_key TEXT PRIMARY KEY,
                holdings TEXT,
                timestamp TEXT
             )""")

def create_user():

	public_key = ''
	private_key = ''
	c.execute(""" INSERT INTO wallets (public_key, private_key) 
		VALUES (?,?)""",(public_key, private_key))
	conn.commit()

def get_user_holdings(public_key):

	c.execute(""" SELECT holdings FROM wallets WHERE public_key = ? """,(public_key))
	holdings = c.fetchall()
	return holdings

def update_user_holdings(private_key, change):

	c.execute(""" UPDATE wallets SET holdings = holdings || ?
	 WHERE private_key = ? """,(holdings,private_key)



