from ecdsa import SigningKey, SECP256k1, VerifyingKey
from eth_utils import keccak
import time

def gen_keys():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    secret_key = private_key.to_string().hex()
    verify_key = public_key.to_string().hex()
    return secret_key,verify_key

def sign(secret_key,msg):
    private_key=SigningKey.from_string(bytes.fromhex(secret_key),curve=SECP256k1)
    signature=private_key.sign(bytes(msg,'utf-8'))
    return signature.hex()

def verify(verify_key,signature,msg):
    verify_key = VerifyingKey.from_string(bytes.fromhex(verify_key), curve=SECP256k1)
    ver=verify_key.verify(bytes.fromhex(signature), bytes(msg, 'utf-8'))
    return ver

def get_address(verify_key):
    h=keccak(verify_key.encode()).hex()
    address='0x'+h[-40:]
    return address

message="SDU2021Project10"

start=time.time()
secret_key,verify_key=gen_keys()
end=time.time()
print("private key:",secret_key)
print("public key:",verify_key)
print("time of public and private key generation:",end-start,"s\n")

start=time.time()
signature=sign(secret_key,message)
end=time.time()
print("siganture:",signature)
print("time of signature generation:",end-start,"s\n")

start=time.time()
assert verify(verify_key,signature,message)
end=time.time()
print("time of verifying signature generation:",end-start,"s\n")

start=time.time()
address=get_address(verify_key)
end=time.time()
print("address:",address)
print("time of verifying signature generation:",end-start,"s\n")







