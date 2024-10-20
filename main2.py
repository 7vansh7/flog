import os
import ecdsa
import hashlib
import json
import time


class Wallet:
    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)
        self.balance = 100  # Example starting balance

    def generate_private_key(self):
        return os.urandom(32)

    def generate_public_key(self, private_key):
        signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        verifying_key = signing_key.verifying_key
        return verifying_key.to_string()

    def get_address(self):
        public_key_hash = hashlib.sha256(self.public_key).hexdigest()
        return public_key_hash[:40]  # Example truncation for address

    def sign_transaction(self, message):
        signing_key = ecdsa.SigningKey.from_string(self.private_key, curve=ecdsa.SECP256k1)
        signature = signing_key.sign(message.encode('utf-8'))
        return signature

    def verify_signature(self, message, signature):
        verifying_key = ecdsa.VerifyingKey.from_string(self.public_key, curve=ecdsa.SECP256k1)
        return verifying_key.verify(signature, message.encode('utf-8'))

    def update_balance(self, amount):
        self.balance += amount

# ---- Transaction Class ----
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def sign_transaction(self, wallet):
        transaction_data = self.to_json()
        self.signature = wallet.sign_transaction(transaction_data)
        return self.signature


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def add_transaction(self, transaction):
        if transaction.signature:
            self.pending_transactions.append(transaction)
            print("Transaction added to pending transactions")
        else:
            print("Invalid transaction: No signature")

    def mine_block(self):
        block = {
            'transactions': [tx.to_dict() for tx in self.pending_transactions],
            'previous_hash': self.chain[-1]['hash'] if self.chain else '0'  # Genesis block case
        }
        block['hash'] = hashlib.sha256(json.dumps(block).encode()).hexdigest()
        self.chain.append(block)
        self.pending_transactions = []  # Clear pending transactions

        print(f"Block mined with hash: {block['hash']}")

    def process_transactions(self, wallets):
        for transaction in self.chain[-1]['transactions']:
            sender_wallet = wallets.get(transaction['sender'])
            recipient_wallet = wallets.get(transaction['recipient'])

            if sender_wallet:
                sender_wallet.update_balance(-transaction['amount'])
            if recipient_wallet:
                recipient_wallet.update_balance(transaction['amount'])



wallet1 = Wallet()  # Sender
wallet2 = Wallet()  # Recipient

wallets = {
    wallet1.get_address(): wallet1,
    wallet2.get_address(): wallet2
}

print(f"Wallet 1 Address: {wallet1.get_address()} | Balance: {wallet1.balance}")
print(f"Wallet 2 Address: {wallet2.get_address()} | Balance: {wallet2.balance}")

# 2. Create a transaction from wallet1 to wallet2
transaction = Transaction(sender=wallet1.get_address(), recipient=wallet2.get_address(), amount=30)
transaction.sign_transaction(wallet1)

print(f"Signed Transaction: {transaction.to_json()}")

# 3. Add the transaction to the blockchain
blockchain = Blockchain()
blockchain.add_transaction(transaction)

# 4. Mine a block and process the transaction
blockchain.mine_block()
blockchain.process_transactions(wallets)

# 5. Display updated balances
print(f"Wallet 1 Address: {wallet1.get_address()} | Updated Balance: {wallet1.balance}")
print(f"Wallet 2 Address: {wallet2.get_address()} | Updated Balance: {wallet2.balance}")

