import sqlite3


conn = sqlite3.connect('./walletDB')
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                public_key TEXT,
                private_key TEXT,
                holdings TEXT,
                timestamp TEXT
             )""")

def add_data():
	pass 

def get_data():
	pass