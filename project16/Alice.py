import math
import socket
from gmpy2 import invert
from os.path import commonprefix
import sm2

p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
x = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

HOST=''
PORT=50007
alice= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
alice.bind((HOST, PORT))
print('Listening on port:',PORT)

# d2
d2=0x2fca0b121feda9849680b861d0170302783a273758e43e93062e563ba5011642

# receive t1
x,addr=alice.recvfrom(1024)
x=int(x.decode(),16)
y,addr=alice.recvfrom(1024)
y=int(y.decode(),16)
t1=(x,y)

# t2=d2^(-1)*t1
t2=sm2.elliptic_mul(x,y,invert(d2,p))
x,y=hex(t2[0]),hex(t2[1])

# send t2
alice.sendto(x.encode(),addr)
alice.sendto(y.encode(),addr)

alice.close()
print("alice close.")
