import sqlite3
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib


conn = sqlite3.connect('./wallets.db', check_same_thread=False)
c = conn.cursor()

c.execute("select * from wallets where public_key = ?",('041dbd159a642ec400e99e992585de03622da20151cb07dd78549566e5610555c6ba9d13818ab85f400d3f2a7674b8e4409273f2bd441c58862643230b7733a5e3',))
print(c.fetchall())


# private_key_testing = '1170f1d9b8df97e17ece686e4ce7155c66650a306a4a0dfb092f11e5e0bac1c4'
# 04addd391c53de0eba0aac9e2400c65b90420b084bd01c70fa7bbaded42e2f749012165a486690a19901931f3a80c4838b91cc500e9394de7f0ea018c128acaf60


# private_key = SigningKey.generate(curve=SECP256k1)
# public_key = private_key.get_verifying_key()

# message = "Send 10 coins to Bob"
# # Hash the message using SHA-256
# message_hash = hashlib.sha256(message.encode('utf-8')).digest()

# # 3. Sign the message hash with the private key
# signature = private_key.sign(message_hash)

# # 4. Verify the signature with the public key
# try:
#     valid = public_key.verify(signature, message_hash)
#     print("Signature is valid:", valid)
# except:
#     print("Signature verification failed.")


# sender 1170f1d9b8df97e17ece686e4ce7155c66650a306a4a0dfb092f11e5e0bac1c4
# 04d3660917e9d912968d529928c652c7023e7a12887eb63dc236fa0065265a7d807726df09beb9a1d23cc42d3eead8a808adea729fefea50d3c7a702f466314da4


# 041dbd159a642ec400e99e992585de03622da20151cb07dd78549566e5610555c6ba9d13818ab85f400d3f2a7674b8e4409273f2bd441c58862643230b7733a5e3
# 7fca3fb86280f346b2c4ed6b0d7d069e6f81902787033d8239a49b3681137ea9


# MAKING a NFT


house_nft = {};