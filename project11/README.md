# 实验原理

    基于RFC6979协议实现sm2

    使用gmssl库中的sm2实现签名，k的选取参考RFC6979

## RF6979

可以将RFC6979的简化版理解为：

`k = SHA256(d + HASH(m))`

## 关键代码

```python
def gen_k(privateKey, data):
    # Converts a string to an array of bytes
    privateKey_bytes = privateKey.encode('utf-8')
    #data_bytes = data.encode('utf-8')

    # Compute HASH(data)
    hash_data = hashlib.sha256(data).digest()

    # Concatenate the string d with HASH(m) to calculate SHA256
    concatenated_bytes = privateKey_bytes + hash_data
    k = hashlib.sha256(concatenated_bytes).hexdigest()

    return k
```


# 运行指导

代码可直接运行

# 运行效果：

签名用时 0.005068063735961914 s

![image](https://github.com/korangar-group42num1/group42/assets/129478905/35279080-8fe7-466b-ac1b-7a679aad6d13)

# 参考文献：

1.https://zhuanlan.zhihu.com/p/55911409

2.https://www.cnblogs.com/pythonywy/p/13638806.html
