import sm2
import sys
import socket
from os.path import commonprefix
from gmpy2 import invert

p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
x = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

HOST='127.0.0.1'
PORT=50007
bob = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
# Connection bob
    bob.connect((HOST, PORT))
except Exception as e:
    print('Bob not found or not open.')
    sys.exit()
addr=(HOST,PORT)
# c=c1||c2||c3
c1=(0xd402d3e95bf1003fa5f236daaf0bd87bd1b43306c9043a90dcebc87f93a318aa,
    0xe86d934c96efa894b5ab22f9c0ae078d7a018feee8ebfb2971a60845964975b8)
c2=0x0d31dff8bac2643c24f6860dd5f02c8f
c3=0xbc860d9281275cf6aa5fa3eec0f6cb1999c1c7d03e1774c07b1140d13fd4d439

c2_len='0d31dff8bac2643c24f6860dd5f02c8f'

# d1
d1=0xb528647adfd8057d137ae8288d75fa6676ade65790c3016d72bb52162e34f1

# t1=d1^(-1)*c1
t1=sm2.elliptic_mul(c1[0],c1[1],invert(d1,p))
x,y=hex(t1[0]),hex(t1[1])
klen=len(c2_len)*4
#print(klen)

# send t1
bob.sendto(x.encode(),addr)
bob.sendto(y.encode(),addr)

# receive t2
x1,addr=bob.recvfrom(1024)
x1=int(x1.decode(),16)
y1,addr=bob.recvfrom(1024)
y1=int(y1.decode(),16)
t2=(x1,y1)

# t2-c1=(x2,y2)
x2,y2=sm2.elliptic_add(t2[0],t2[1],c1[0],-c1[0])
x2='0'*(256-len(bin(x2)[2:]))+bin(x2)[2:]
y2='0'*(256-len(bin(y2)[2:]))+bin(y2)[2:]
t=sm2.KDF(x2+y2,klen)

# m''=c2⨁t
m2=c2^int(t,2)
u=sm2.sm3_hash(x2+str(bin(m2)[2:])+y2)
print("decrypt:",hex(m2)[2:])

bob.close()
print("Bob close.")




