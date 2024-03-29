# 实验内容

**Project15: implement sm2 2P sign with real network communication**

# 运行指导

将文件夹中 **sm2.py,Alice.py,Bob.py** 文件添加至同一文件夹中，先运行**Alice.py**，再运行**Bob.py**，即可协同生成sm2签名

# 实验原理

**SM2协同签名方案**如图所示

![SM2协同签名方案](https://github.com/korangar-group42num1/group/assets/129478905/4a3feb01-73b5-4667-8a5e-4e00423f4f7c)

## P1

![image](https://github.com/korangar-group42num1/group/assets/129478905/71f6a4c1-0f8d-4212-94c0-f2b3f4aead76)

### 代码实现

#### Bob

```python
# Generate sub private key d1
d1=random.randint(1,n-1)

# Compute p1=d1^(-1)·G
p1=sm2.elliptic_mul(X,Y,invert(d1,p))
x,y=hex(p1[0]),hex(p1[1])

# (1) Send p1
addr = (HOST, PORT)
bob.sendto(x.encode(),addr)
bob.sendto(y.encode(),addr)
```

#### Alice

```python
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
```

## Q1,e

![image](https://github.com/korangar-group42num1/group/assets/129478905/967a4c1a-181b-40e2-8526-3277c968565e)

### 代码实现

#### Bob

```python
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
```

#### Alice

```python
# Receive q1,e
x,addr=alice.recvfrom(1024)
x=int(x.decode(),16)
y,addr=alice.recvfrom(1024)
y=int(y.decode(),16)
q1=(x,y)
e,addr=alice.recvfrom(1024)
e=int(e.decode(),16)
```

## r,s2,s3

![image](https://github.com/korangar-group42num1/group/assets/129478905/797f3f8b-0e22-4991-b71c-d6315fd707fe)

### 代码实现

#### Alice

```python
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

```

#### Bob

```pyhton
# Receive r,s2,s3
r,addr=bob.recvfrom(1024)
r=int(r.decode(),16)

s2,addr=bob.recvfrom(1024)
s2=int(s2.decode(),16)

s3,addr=bob.recvfrom(1024)
s3=int(s3.decode(),16)
```

## 计算签名

![image](https://github.com/korangar-group42num1/group/assets/129478905/2f786edd-ee2f-4024-a8a5-3b257ad88107)

### 代码实现

#### Bob

```python
# (5) Generate signature (r,s)
# Compute s=(d1*k1)*s2+d1*s3-r mod n
s=((d1*k1)*s2+d1*s3-r)%n

# If s ≠ 0 or s ≠ n − r，output signature = (r, s)
if(s!=0 or s!=n-r):
    print("signature:")
    print(hex(r))
    print(hex(s))
```

# 运行效果

![image](https://github.com/korangar-group42num1/group/assets/129478905/6c091e92-1202-4c4b-b216-bdd7f2a3b6c1)


# 参考资料

1. https://blog.csdn.net/xiaofengdada/article/details/122684715?ops_request_misc
   
2. https://blog.csdn.net/keyboardlabourer/article/details/128917468?ops_request_misc

3. 课程ppt:20230401-sm2-public

