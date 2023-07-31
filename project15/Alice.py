import socket
from os.path import commonprefix
import random
import sm2
from gmpy2 import invert

# Elliptic curve parameter
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

HOST = ''
PORT = 50007
alice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
alice.bind((HOST, PORT)) # Binding socket
print('Listening on port:',PORT)

#  (1) Generate sub private key d2
d2=random.randint(1,n-1)

# Receive p1
x,addr=alice.recvfrom(1024)
x=int(x.decode(),16)
y,addr=alice.recvfrom(1024)
y=int(y.decode(),16)

#  (2) Generate shared public key: compute p = d2^(-1)·p1-G
p1=(x,y)
p=sm2.elliptic_mul(p1[0],p1[1],invert(d2,p))
p=sm2.elliptic_add(p[0],p[1],X,-Y)

# Receive q1,e
x,addr=alice.recvfrom(1024)
x=int(x.decode(),16)
y,addr=alice.recvfrom(1024)
y=int(y.decode(),16)
q1=(x,y)
e,addr=alice.recvfrom(1024)
e=int(e.decode(),16)

# (4) Generate partial signature r
# Randomly generate k2 k3
k2=random.randint(1,n-1)
k3=random.randint(1,n-1)

# Calculate q2=k2·G
q2=sm2.elliptic_mul(X,Y,k2)

# Calculate k3·q1+q2=(x1,y1)
x1,y1=sm2.elliptic_mul(q1[0],q1[1],k3)
x1,y1=sm2.elliptic_add(x1,y1,q2[0],q2[1])

# r=x1+e mod n
r=(x1+e)%n

# s2=d2*k3 mod n
s2=(d2*k3)%n

# s3=d2*(r+k2) mod n
s3=(d2*(r+k2))%n

# Send r,s2,s3
alice.sendto(hex(r).encode(),addr)
alice.sendto(hex(s2).encode(),addr)
alice.sendto(hex(s3).encode(),addr)

# Close connection
alice.close()
print("Alice close.")






