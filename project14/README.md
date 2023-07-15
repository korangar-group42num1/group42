# 实验原理

## PGP

此代码中对称加密算法使用`AES`，非对称加密算法使用`SM2`，压缩函数采用`SHA-256`

![image](https://github.com/korangar-group42num1/group42/assets/129478905/65c8ec14-112a-471a-afe4-a03df561978b)

### 代码说明

1.生成会话密钥

 ```php {.line-numbers}
session_key = get_random_bytes(16)
 ```

2.压缩消息 

 ```php {.line-numbers} 
 hash_data = hashlib.sha256(data).digest()
 ```

3.用会话密钥和 AES 加密压缩后的消息

 ```php {.line-numbers} 
 iv = get_random_bytes(16)
 cipher = AES.new(session_key, AES.MODE_CBC, iv)
 ciphertext_aes = cipher.encrypt(pad(hash_data, AES.block_size))
 ```

4.用 sm2 加密会话密钥

 ```php {.line-numbers} 
sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
ciphertext_sm2 = sm2_crypt.encrypt(session_key)
 ```

5.将前两步生成的消息拼合在一起，转为文本消息，即为加密后消息

 ```php {.line-numbers} 
ciphertext=(ciphertext_sm2+ciphertext_aes).hex().encode('utf-8')
```

# 运行指导

代码可直接运行

# 运行效果

加密用时 0.0009996891021728516 s

![image](https://github.com/korangar-group42num1/group42/assets/129478905/a0af10f0-10e2-4d8c-9c93-cf6df56f96ed)



# 参考资料

1.https://blog.csdn.net/chengqiuming/article/details/83047116
