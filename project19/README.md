# 实验内容

**Project19: forge a signature to pretend that you are Satoshi**

# 运行指导

代码可直接运行

# 实验原理

![image](https://github.com/korangar-group42num1/group/assets/129478905/3a57558b-6920-4a38-add4-08d6748f5ae5)

## 伪造过程

### 随机选择 u,v∈(1,n-1)

![u,v](https://github.com/korangar-group42num1/group/assets/129478905/c116036c-a937-4454-8f98-010469bf83cd)


### 计算 R'=(x',y')=u*G+v*P

![R'](https://github.com/korangar-group42num1/group/assets/129478905/2b088b51-8af7-4a15-bb65-cc52d56d9775)


### e' = r' * u * v^(-1) mod n

### s' = r' * v^(-1) mod n

![r',s'](https://github.com/korangar-group42num1/group/assets/129478905/f436690b-fe3c-4cda-8dd8-e68161681775)

## 关键代码

```python
def forge(n,G,P):
    u=randint(1,n-1)
    v=randint(1,n-1)
    r_cap=u*G+v*P
    r_=(r_cap.x())%n
    s_=(r_*invert(v,n))%n
    e_=(s_*u)%n
    signature_=ecdsa.ecdsa.Signature(r_,s_)

    return e_,r_,s_,signature_
```

# 运行效果

![image](https://github.com/korangar-group42num1/group/assets/129478905/9430cdd3-3a81-468a-8f82-8ae7cea8ba89)


# 参考资料

1.https://blog.csdn.net/m0_57291352/article/details/123486909

2.课程ppt：20230401-btc-public

