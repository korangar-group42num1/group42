# 项目内容

**Project10: report on the application of this deduce technique in Ethereum with ECDSA**

# ECDSA

## 概述

**ECDSA** ( Elliptic Curve Digital Signature Algorithm ) 是一个基于**椭圆曲线**的签名算法。对某个消息进行签名的目的是使接收者确认该消息是由签名者发送的，且未经过篡改。

椭圆曲线数字签名算法（**ECDSA**）是使用椭圆曲线密码（**ECC**）对数字签名算法（**DSA**）的模拟。ECDSA于1999年成为ANSI标准，并于2000年成为IEEE和NIST标准。

它在1998年既已为ISO所接受，并且包含它的其他一些标准亦在ISO的考虑之中。与普通的离散对数问题（discrete logarithm problem DLP）和大数分解问题（integer factorization problem IFP）不同，椭圆曲线离散对数问题（elliptic curve discrete logarithm problem ECDLP）没有亚指数时间的解决方法。因此椭圆曲线密码的单位比特强度要高于其他公钥体制。

数字签名算法（DSA）在联邦信息处理标准FIPS中有详细论述，称为数字签名标准。它的安全性基于**素域上的离散对数问题**。椭圆曲线密码（ECC）由Neal Koblitz和Victor Miller于1985年发明。它可以看作是椭圆曲线对先前基于离散对数问题（DLP）的密码系统的模拟，只是群元素由素域中的元素数换为有限域上的椭圆曲线上的点。

椭圆曲线密码体制的安全性基于**椭圆曲线离散对数问题（ECDLP）的难解性**。椭圆曲线离散对数问题远难于离散对数问题，椭圆曲线密码系统的单位比特强度要远高于传统的离散对数系统。因此在使用较短的密钥的情况下，ECC可以达到于DL系统相同的安全级别。这带来的好处就是计算参数更小，密钥更短，运算速度更快，签名也更加短小。因此椭圆曲线密码尤其适用于处理能力、存储空间、带宽及功耗受限的场合。

## 原理

ECDSA是ECC与DSA的结合，整个签名过程与DSA类似，所不一样的是签名中采取的算法为ECC，最后签名出来的值也是分为r,s。


# 以太坊

## 概述

以太坊（Ethereum）是一个建立在区块链技术之上， 去中心化应用平台。它允许任何人在平台中建立和使用通过区块链技术运行的去中心化应用。

从计算机科学的角度来说，以太坊是一种确定性但实际上无界的状态机，它有两个基本功能，第一个是全局可访问的单例状态，第二个是对状态进行更改的虚拟机。

从更实际的角度来说，以太坊是一个开源的，全球的去中心化计算架构，执行成为 智能合约 的程序。它使用区块链来从同步和存储系统 状态，以及称为 ether 的
加密货币来计量和约束执行资源成本。

以太坊平台使开发人员能够利用内置的经济学方法构建强大的去中心化应用程序。在保证持续正常运行时间的同时，还可以减少或消除审查机构，第三方接口和对手方风险。


# ECDSA在以太坊中的作用

ECDSA在以太坊中的作用包括：

**以太坊地址**

**智能合约**

**数字签名**

## 以太坊地址

一般来说，这代表一个 EOA 或合约，它可以在区块链上接收（目标地址）或发送（源地址）交易。

更具体地说，它是 **ECDSA 公钥**的 Keccak 散列的最右边的160位，表现为16进制的40个字符长度，在前面加上“0x”字符。

### 代码实现

```php
def get_address(verify_key):
    h=keccak(verify_key.encode()).hex()
    address='0x'+h[-40:]
    return address
```

## 智能合约

以太坊智能合约是区块链技术的关键组成部分之一，它被用于构建去中心化应用程序（DApp）和智能合约平台。

然而智能合约的安全漏洞是在以太坊区块链上最阻碍普及的障碍之一，在最近的几年中，已经发现了许多智能合约漏洞，

例如DAO攻击、Parity钱包漏洞，导致数百万美元的资金损失。

在防范智能合约的安全漏洞方面，使用多种加密技术很重要。

智能合约的安全与其加密的强度直接相关，建议使用 SHA3、ECDSA 和AES等多种加密技术，以提高智能合约的安全性，

**ECDSA**在其中发挥重要作用。

## 数字签名

以太坊使用ECDSA来确保资金只能由合法所有者使用，ECDSA是用于基于椭圆曲线私钥/公钥对的数字签名的算法。

数字签名是一种数学签名，由两部分组成：

```
1. 是使用私钥（签名密钥）从消息（交易）中创建签名的算法。
   
2. 是允许任何人仅使用消息和公钥来验证签名的算法。
```

数字签名在以太坊中有三种用途：
```
1.签名证明私钥的所有者，暗示着以太坊账户的所有者，已经授权支付ether或执行合约。

2.授权的证明是_undeniable_（不可否认）。

3.签名证明交易数据在交易签名后没有也不能被任何人修改。
```
### 数字签名工作流程

#### 签名过程

![image](https://github.com/korangar-group42num1/group/assets/129478905/5adb128c-0984-4b15-a1f9-df8b72990676)


1. 选择一条椭圆曲线**Ep(a,b)**，和基点**G**；
    
2. 选择私有密钥**k（k<n，n为G的阶）**，利用基点**G**计算公开密钥K=kG；
    
3. 产生一个随机整数**r（r<n）**，计算点**R=rG**；
    
4. 将原数据和点R的坐标值x,y作为参数，计算SHA1做为hash，即**Hash=SHA1(原数据,x,y)**；
    
5. 计算**s≡r - Hash * k (mod n)**
    
6. r和s做为签名值，如果**r和s其中一个为0**，重新从第3步开始执行

#### 验证过程

![image](https://github.com/korangar-group42num1/group/assets/129478905/31cd758a-5546-49aa-a3d2-eb695768774c)


1. 接受方在收到消息(m)和签名值(r,s)后，进行以下运算
    
2. 计算：**sG+H(m)P=(x1,y1), r1≡ x1 mod p**
    
3. 验证等式：**r1 ≡ r mod p**
    
4. 如果等式成立，接受签名，否则签名无效。

#### 代码实现

1. 初始化化秘钥组，生成ECDSA算法的公钥和私钥
   
2. 执行私钥签名， 使用私钥签名，生成私钥签名
 
3. 执行公钥签名，生成公钥签名
 
4. 使用公钥验证私钥签名
   
```php
def sign(secret_key,msg):
    private_key=SigningKey.from_string(bytes.fromhex(secret_key),curve=SECP256k1)
    signature=private_key.sign(bytes(msg,'utf-8'))
    return signature.hex()

def verify(verify_key,signature,msg):
    verify_key = VerifyingKey.from_string(bytes.fromhex(verify_key), curve=SECP256k1)
    ver=verify_key.verify(bytes.fromhex(signature), bytes(msg, 'utf-8'))
    return ver
```

# 运行效果

![image](https://github.com/korangar-group42num1/group/assets/129478905/1973ccac-4ed3-422a-b1d5-41958ee80328)


# ECDSA 的优势

与经典的RSA、DSA等公钥密码体制相⽐，椭圆密码体制有以下优点

## 安全性能更⾼

160位ECC加密算法的安全强度相当于1024位RSA加密；

210位ECC加密算法的安全强度相当于2048位RSA加密。

## 处理速度快

计算量⼩，处理速度快 在私钥的处理速度上（解密和签名），ECC远 ⽐RSA、DSA快得多。

## 存储空间占用小

ECC的密钥尺⼨和系统参数与RSA、DSA相⽐要⼩得多， 所以占⽤的存储空间⼩得多。

带宽要求低使得ECC具有⼴泛的应⽤前景。ECC的这些特点使它必将取代RSA，成为通⽤的公钥加密算法。


# 参考资料

1. https://blog.csdn.net/PUPPET4/article/details/105528411?spm
2. https://www.bookstack.cn/read/ethereum_book-zh 
3. https://blog.csdn.net/sanqima/article/details/122143585
4. https://ethereum.org/zh/
5. https://github.com/Archer-One/Implementation-of-digital-signature-algorithm
6. https://blog.csdn.net/wolfjson/article/details/126753011?utm_medium
7. 课程ppt：20230407-eth-public 
