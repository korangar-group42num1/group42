# 实验内容

**Project21: Schnorr Bacth**

# 运行指导

将文件夹内代码 **Schnorr.py** 和 **secp256k1.py**添加至同一目录内，可直接运行

# 实验原理

## Schnorr签名

签名以及验签流程如下图所示

![image](https://github.com/korangar-group42num1/group42/assets/129478905/c1a8cb6d-c1be-49a3-82ab-404ecea20a54)

每个签名单独验证，在签名量巨大的情况下，会导致时间空间开销过大。
Schnorr Batch通过将多个签名的计算合并为一个集合，进行批量处理，提高效率。

## Schnorr Batch

Schnorr Batch 流程如图所示

![image](https://github.com/korangar-group42num1/group42/assets/129478905/3080dc44-be6a-43f1-a5ae-e896625ee674)

### 关键代码

```python
import hashlib
import random
import secp256k1

prikey = secp256k1.Fr(0x5f6717883bef25f45a129c11fcac1567d74bda5a9ad4cbffc8203c0da2a1473c)
pubkey = secp256k1.G * prikey

# Hash of messages.
with open('./secp256k1.py', 'rb') as f:
    m = int.from_bytes(hashlib.sha256(f.read()).digest(), 'little')
    m = secp256k1.Fr(m)
print(f'hash={m}')

# R = k ∗ G
# e = hash(R || m)
# s = k + e ∗ prikey
k = secp256k1.Fr(random.randint(0, secp256k1.N))
R = secp256k1.G * k
hasher = hashlib.sha256()
hasher.update(R.x.x.to_bytes(32, 'little'))
hasher.update(R.y.x.to_bytes(32, 'little'))
hasher.update(m.x.to_bytes(32, 'little'))
e = secp256k1.Fr(int.from_bytes(hasher.digest(), 'little'))
s = k + e * prikey
print(f'sign=(R={R}, s={s})')

# s ∗ G =? R + hash(R || m) ∗ P
verify = secp256k1.G * s == R + pubkey * e
print(f'verify={verify}')
```

# 运行效果

![image](https://github.com/korangar-group42num1/group42/assets/129478905/133e0770-ff4a-49ef-930b-ff68785199a6)

# 参考资料

1.https://blog.csdn.net/weixin_43851783/article/details/124116643 

2.http://accu.cc/content/cryptography/schnorr/

3.课程ppt：20230401-btc-public


