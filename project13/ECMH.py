import math
from gmpy2 import invert
from random import randint
from gmssl import sm3
import time 

# Elliptic curve parameter
#Fp
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
#G=(X,Y) ord(G)=n
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2



# Addition on elliptic curves (x,y)=(x1,y1)+(x2,y2)
def elliptic_add(x1,y1,x2,y2):
    if x1 == x2 and y1 == p-y2:
        return False
    if x1!=x2:
        r=((y2 - y1) * invert(x2 - x1, p))%p
    else:
        r=(((3 * x1 * x1 + a)%p) * invert(2 * y1, p))%p
        
    x = (r * - x1 - x2)%p
    y = (r * (x1 - x) - y1)%p
    return x,y

# The dot product on an elliptic curve k*(x,y)
def elliptic_mul(x,y,k):
    k = k%p
    k = bin(k)[2:]
    rx,ry = x,y
    for i in range(1,len(k)):
        rx,ry = elliptic_add(rx, ry, rx, ry)
        if k[i] == '1':
            rx,ry = elliptic_add(rx, ry, x, y)
    return rx%p,ry%p

def sm3_hash(msg):
    msg=msg.encode()
    msg=bytearray(msg)
    h = sm3.sm3_hash(msg)
    return h

def hash_to_point(msg):
    k = sm3_hash(msg)
    k = int(k,16)%n
    hash_x,hash_y = elliptic_mul(X,Y,k)
    return hash_x,hash_y


message1='SDU2021'
message2='Project13'

start=time.time()
point_1=hash_to_point(message1)
point_2=hash_to_point(message2)

hash_add_point_x,hash_add_point_y=elliptic_add(point_1[0],point_1[1],point_2[0],point_2[1])
end=time.time()

print("hash({a}) + hash({b}) = (",hex(hash_add_point_x),",",hex(hash_add_point_y),")")
print("time:",end-start,'s')


    








