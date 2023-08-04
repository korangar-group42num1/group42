import hashlib
import random
import secp256k1

prikey = secp256k1.Fr(0x5f6717883bef25f45a129c11fcac1567d74bda5a9ad4cbffc8203c0da2a1473c)
pubkey = secp256k1.G * prikey

# Hash of messages.
with open('./secp256k1.py', 'rb') as f:
    m = int.from_bytes(hashlib.sha256(f.read()).digest(), 'little')
    m = secp256k1.Fr(m)
print(f'hash={m}')

# R = k ∗ G
# e = hash(R || m)
# s = k + e ∗ prikey
k = secp256k1.Fr(random.randint(0, secp256k1.N))
R = secp256k1.G * k
hasher = hashlib.sha256()
hasher.update(R.x.x.to_bytes(32, 'little'))
hasher.update(R.y.x.to_bytes(32, 'little'))
hasher.update(m.x.to_bytes(32, 'little'))
e = secp256k1.Fr(int.from_bytes(hasher.digest(), 'little'))
s = k + e * prikey
print(f'sign=(R={R}, s={s})')

# s ∗ G =? R + hash(R || m) ∗ P
verify = secp256k1.G * s == R + pubkey * e
print(f'verify={verify}')
