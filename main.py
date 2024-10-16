import hashlib
import json
import time
import sqlite3

# Connect to the database
conn = sqlite3.connect('blockchain.db')
c = conn.cursor()

# Create tables for blocks and transactions
c.execute('''CREATE TABLE IF NOT EXISTS blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                block_index INTEGER,
                previous_hash TEXT,
                timestamp TEXT,
                hash TEXT,
                nonce INTEGER
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                block_id INTEGER,
                sender TEXT,
                receiver TEXT,
                amount REAL,
                status TEXT,
                FOREIGN KEY(block_id) REFERENCES blocks(id)
             )''')


conn.commit()


class Block:
    def __init__(self, block_index, previous_hash, timestamp, transactions, nonce=0):
        self.block_index = block_index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def save_to_db(self):
        """Save the block and its transactions to the database."""
        c.execute("INSERT INTO blocks (block_index, previous_hash, timestamp, hash, nonce) VALUES (?, ?, ?, ?, ?)",
                  (self.block_index, self.previous_hash, self.timestamp, self.hash, self.nonce))
        block_id = c.lastrowid


        for txn in self.transactions:
            c.execute("INSERT INTO transactions (block_id, sender, receiver, amount, status) VALUES (?, ?, ?, ?, ?)",
                      (block_id, txn['sender'], txn['receiver'], txn['amount'], txn['status']))
        
        conn.commit()


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block (genesis block) and save it to the database."""
        c.execute("SELECT * FROM blocks WHERE block_index = 0")
        genesis_block = c.fetchone()

        if not genesis_block:
            genesis_block = Block(0, "0", time.time(), [])
            genesis_block.save_to_db()

    def get_last_block(self):
        """Retrieve the last block from the database."""
        c.execute("SELECT * FROM blocks ORDER BY id DESC LIMIT 1")
        block_data = c.fetchone()
        return Block(block_data[1], block_data[2], block_data[3], self.load_transactions(block_data[0]), block_data[5])

    def load_transactions(self, block_id):
        """Load transactions for a specific block."""
        c.execute("SELECT * FROM transactions WHERE block_id = ?", (block_id,))
        return [{'sender': txn[2], 'receiver': txn[3], 'amount': txn[4], 'status': txn[5]} for txn in c.fetchall()]

    def add_transaction(self, transaction):
        self.current_transactions.append(transaction)

    def mine_block(self):
        """Simulates mining a new block."""
        last_block = self.get_last_block()
        new_block = Block(
            block_index=last_block.block_index + 1,
            previous_hash=last_block.hash,
            timestamp=time.time(),
            transactions=self.current_transactions
        )
        new_block.save_to_db()
        self.current_transactions = []  # Clear the transaction list after adding the block
        return new_block

    def is_chain_valid(self):
        """Check if the blockchain is valid."""
        c.execute("SELECT * FROM blocks ORDER BY id ASC")
        blocks = c.fetchall()
        
        for i in range(1, len(blocks)):
            current_block = blocks[i]
            previous_block = blocks[i - 1]

            current_block_obj = Block(current_block[1], current_block[2], current_block[3], self.load_transactions(current_block[0]), current_block[5])
            previous_block_obj = Block(previous_block[1], previous_block[2], previous_block[3], self.load_transactions(previous_block[0]), previous_block[5])

            if current_block_obj.hash != current_block_obj.calculate_hash():
                return False

            if current_block_obj.previous_hash != previous_block_obj.hash:
                return False

        return True


class SmartContract:
    def __init__(self, contract_logic):
        """SmartContract with basic logic."""
        self.contract_logic = contract_logic

    def execute(self, *args):
        """Executes the contract logic."""
        return self.contract_logic(*args)

# Simple example contract: Smart Contract that transfers tokens
def transfer_tokens(contract_args):
    sender, receiver, amount = contract_args
    print(f"Transferring {amount} tokens from {sender} to {receiver}")
    return {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "status": "success"
    }

# Define a method to simulate blockchain with smart contracts
def run_blockchain_with_smart_contracts():
    # Initialize blockchain
    blockchain = Blockchain()

    # Create a smart contract for transferring tokens
    token_contract = SmartContract(transfer_tokens)

    # Define some transactions (user interactions with the contract)
    contract_result_1 = token_contract.execute(("Alice", "Bob", 50))
    blockchain.add_transaction(contract_result_1)

    contract_result_2 = token_contract.execute(("Bob", "Charlie", 30))
    blockchain.add_transaction(contract_result_2)

    # Mine a block (includes transactions)
    new_block = blockchain.mine_block()

    # Output the details of the new block
    print(f"Block #{new_block.block_index} has been mined!")
    print(f"Hash: {new_block.hash}")
    print(f"Previous Hash: {new_block.previous_hash}")
    print(f"Transactions: {new_block.transactions}")

    # Check if blockchain is valid
    print(f"Is the blockchain valid? {blockchain.is_chain_valid()}")

# Run the blockchain simulation
run_blockchain_with_smart_contracts()
