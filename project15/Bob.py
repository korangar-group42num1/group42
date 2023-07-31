import socket
from os.path import commonprefix
import random
import sm2
from gmssl import sm3
from gmpy2 import invert
import sys

# Elliptic curve parameter
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

# Calculate the SM3 hash
def sm3_hash(msg):
    msg=msg.encode()
    msg=bytearray(msg)
    h = sm3.sm3_hash(msg)
    return h

HOST = '127.0.0.1'
PORT = 50007
bob = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
# Connection bob
    bob.connect((HOST, PORT))
except Exception as e:
    print('Bob not found or not open.')
    sys.exit()
    
# Generate sub private key d1
d1=random.randint(1,n-1)

# Compute p1=d1^(-1)·G
p1=sm2.elliptic_mul(X,Y,invert(d1,p))
x,y=hex(p1[0]),hex(p1[1])

# (1) Send p1
addr = (HOST, PORT)
bob.sendto(x.encode(),addr)
bob.sendto(y.encode(),addr)

# (3) Set z to be identifier for both parties, message is m
m="SDU2021Project15"
z="_bob"
e=sm3_hash(m+z)

# Randomly generate k1
k1=random.randint(1,n-1)

# Compute q1=k1·G
q1=sm2.elliptic_mul(X,Y,k1)
x,y=hex(q1[0]),hex(q1[1])

# Send q1,e
bob.sendto(x.encode(),addr)
bob.sendto(y.encode(),addr)
bob.sendto(e.encode(),addr)

# Receive r,s2,s3
r,addr=bob.recvfrom(1024)
r=int(r.decode(),16)

s2,addr=bob.recvfrom(1024)
s2=int(s2.decode(),16)

s3,addr=bob.recvfrom(1024)
s3=int(s3.decode(),16)

# (5) Generate signature (r,s)
# Compute s=(d1*k1)*s2+d1*s3-r mod n
s=((d1*k1)*s2+d1*s3-r)%n

# If s ≠ 0 or s ≠ n − r，output signature = (r, s)
if(s!=0 or s!=n-r):
    print("signature:")
    print(hex(r))
    print(hex(s))

# Close connection
bob.close()
print("Bob close.")





