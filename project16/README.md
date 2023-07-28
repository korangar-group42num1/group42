# 实验内容 

**Project16: implement sm2 2P decrypt with real network communication**

# 运行指导

将文件夹中**sm2.py,Alice.py,Bob.py** 添加至同一目录，先运行**Alice.py**，再运行**Bob.py**，可得到结果

# 实验原理

解密过程如图所示

![image](https://github.com/korangar-group42num1/group/assets/129478905/29c97f27-d737-4670-81b4-d2d66c403d6f)

## T1

![image](https://github.com/korangar-group42num1/group/assets/129478905/72a963e1-94b5-4ff3-a90a-0dba41f83ae5)

### 代码实现

#### Bob

```python
# t1=d1^(-1)*c1
t1=sm2.elliptic_mul(c1[0],c1[1],invert(d1,p))
x,y=hex(t1[0]),hex(t1[1])
klen=len(c2_len)*4
#print(klen)

# send t1
bob.sendto(x.encode(),addr)
bob.sendto(y.encode(),addr)
```

#### Alice

```python
# receive t1
x,addr=alice.recvfrom(1024)
x=int(x.decode(),16)
y,addr=alice.recvfrom(1024)
y=int(y.decode(),16)
t1=(x,y)
```

## T2

![image](https://github.com/korangar-group42num1/group/assets/129478905/7b81ba0b-48cc-4b14-8a3b-dc15bf027b68)

### 代码实现

#### Alice

```python
# t2=d2^(-1)*t1
t2=sm2.elliptic_mul(x,y,invert(d2,p))
x,y=hex(t2[0]),hex(t2[1])

# send t2
alice.sendto(x.encode(),addr)
alice.sendto(y.encode(),addr)
```

#### Bob

```python
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
```

# 运行效果

![image](https://github.com/korangar-group42num1/group/assets/129478905/5332e8d4-9e6b-4af3-83fe-250274965546)

# 参考资料

1.https://blog.csdn.net/Heidlyn/article/details/53993002?ops_request_misc

2.课程ppt:20230401-sm2-public
