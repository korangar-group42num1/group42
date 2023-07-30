import ecdsa
from random import randint
from gmpy2 import invert
from math import gcd
import time

def forge(n,G,P):
    u=randint(1,n-1)
    v=randint(1,n-1)
    r_cap=u*G+v*P
    r_=(r_cap.x())%n
    s_=(r_*invert(v,n))%n
    e_=(s_*u)%n
    signature_=ecdsa.ecdsa.Signature(r_,s_)

    return e_,r_,s_,signature_

start=time.time()
g_cap=ecdsa.SECP256k1.generator
n=g_cap.order()
d=randint(1,n-1)
public_key=ecdsa.ecdsa.Public_key(g_cap,g_cap*d)
private_key=ecdsa.ecdsa.Private_key(public_key,d)

p_cap=public_key.point
e_,r_,s_,signature_=forge(n,g_cap,p_cap)

assert public_key.verifies(e_,signature_)
end=time.time()

print("Forged signature succeeded.")
print("signature:",hex(r_)[2:]+hex(s_)[2:])
print("time:",end-start,"s.")



