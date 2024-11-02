import sqlite3
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib


# conn = sqlite3.connect('./wallets.db', check_same_thread=False)
# c = conn.cursor()

# c.execute("select * from wallets where public_key = ?",('04d3660917e9d912968d529928c652c7023e7a12887eb63dc236fa0065265a7d807726df09beb9a1d23cc42d3eead8a808adea729fefea50d3c7a702f466314da4',))
# print(c.fetchall())


# private_key_testing = '1170f1d9b8df97e17ece686e4ce7155c66650a306a4a0dfb092f11e5e0bac1c4'

private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.get_verifying_key()

message = "Send 10 coins to Bob"
# Hash the message using SHA-256
message_hash = hashlib.sha256(message.encode('utf-8')).digest()

# 3. Sign the message hash with the private key
signature = private_key.sign(message_hash)

# 4. Verify the signature with the public key
try:
    valid = public_key.verify(signature, message_hash)
    print("Signature is valid:", valid)
except:
    print("Signature verification failed.")