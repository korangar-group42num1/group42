# 实验内容

**Project13: Implement the above ECMH scheme**

![image](https://github.com/korangar-group42num1/group42/assets/129478905/74cb7084-94fa-4cb9-a7ad-36bad351f72e)

# 运行指导

代码可直接运行

# 实验原理 

将消息的**哈希值**（此处采用sm3）各自**映射**到椭圆曲线上，计算出其坐标，采用椭圆曲线上的加法进行计算。

## 关键代码

### 加法

```python
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
```
### 乘法

```python
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

```

### 映射

```python
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
```

# 运行结果

![image](https://github.com/korangar-group42num1/group42/assets/129478905/fcfba02a-683f-4d5b-9af4-cdb7a55bd984)

# 参考资料

1.https://blog.csdn.net/lanvender55/article/details/108704853 

2.课程ppt：20230401-sm2-public





