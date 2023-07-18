# 实验内容

**Project3: implement length extension attack for SM3, SHA256, etc.**

# 实验原理

## SM3

SM3 密码杂凑算法是中国国家密码管理局 2010 年公布的中国商用密码杂凑算法标准。适用于商用密码应用中的数字签名和验证。
SM3 是在 SHA-256 基础上改进实现的一种算法，其安全性和 SHA-256 相当。SM3 和 MD5 的迭代过程类似，也采用 **Merkle-Damgard结构** 。
消息分组长度为512位，摘要值长度为256位。
整个算法执行过程分四个步骤：**消息填充、消息扩展、迭代压缩、输出结果**

## 长度扩展攻击（Length Extension Attack）

![Length Extension Attack](https://github.com/korangar-group42num1/group/assets/129478905/5bff1edd-3292-48fe-bb72-561032063713)

长度扩展攻击是基于**Merkle-Damgard结构**的一种攻击方式。对于消息msg，攻击者知道**msg的哈希值hash(msg)** 和一个**任意的其他消息（ext）**,
不需要知道msg就可以计算出**hash(msg_padding||ext_padding)**

    1.用hash(msg)替代标准sm3中的iv，计算hash_(ext)
    
    2.计算hash(msg_padding||ext_padding)
    
    3.若hash_(ext)==hash(msg_padding||ext_padding)，则攻击成功

# 代码实现

## 运行指导

将sm3.py和Length_Extensiona_Attack.py添加到同一目录下，可直接运行。

## 关键代码说明

### 长度扩展攻击

用msg_hash作为初始向量加密msg_ext

```php {.line-numbers} 
def length_extension_attack(msg_hash,msg_ext):
    iv_new=[]
    for i in range(0,8):
        iv_new.append(int(msg_hash[8*i:8*(i+1)],16))        
    msg_ext_hash=sm3.sm3(msg_ext,iv_new)
    return msg_ext_hash
```

### 计算hash(msg_padding||ext_padding)

用于验证攻击的正确性。
若与该函数的返回值与长度拓展攻击的返回值相等，则攻击成功

```php {.line-numbers} 
def verify_length_extension_attack(msg,ext):
    msg_padding=sm3.padding(message.encode().hex())
    ext_padding=sm3.padding(ext.encode().hex())
    set_512=sm3.get_set(msg_padding+ext_padding)
    v_hash=sm3.iterative_compression(set_512,iv)
    sm3_hash=''
    for i in range(0,len(v_hash)):
        sm3_hash+=(8-len(hex(v_hash[i])[2:]))*'0'
        sm3_hash+=hex(v_hash[i])[2:]
    return sm3_hash
```

# 运行效果

如图，对于 8000 bits 的原始消息和 3200 bit s的扩展消息，计算 hash(msg_padding||ext_padding) 的时间是0.007059574127197266 s

![image](https://github.com/korangar-group42num1/group/assets/129478905/1c508863-8de4-4031-a114-d3bb5b450821)


# 参考资料

1.http://www.sca.gov.cn/sca/xwdt/2010-12/17/1002389/files/302a3ada057c4a73830536d03e683110.pdf

2.课程ppt：20230330-sm3-public

