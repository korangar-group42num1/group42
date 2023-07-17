# 运行指导
    1.安装开源库openssl并配置在vs中
    2.将代码添加到同一项目内，可直接运行
  
# 实验原理

运用开源库**openssl**实现SM4的软件实现（ecb模式）

## 加密 long encrypt

1.初始化上下文

```php {.line-numbers} 
EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
EVP_CIPHER_CTX_init(ctx);
```
2.工作模式

工作模式为ECB模式

```php {.line-numbers}
const EVP_CIPHER* cipher = EVP_sm4_ecb();
```
3.初始化加密操作

```php {.line-numbers}
EVP_EncryptInit_ex(ctx, cipher, NULL, key, NULL);
```
4.加密

```php {.line-numbers}
long len;
EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len);
long ciphertext_len = len;
EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
ciphertext_len += len;
```
5.清理上下文

```php {.line-numbers}
EVP_CIPHER_CTX_free(ctx);
```

6.返回加密后的数据

## 解密 long decrypt

1.初始化上下文

```php {.line-numbers}
EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
EVP_CIPHER_CTX_init(ctx);
```
2.工作模式

工作模式为ECB模式

```php {.line-numbers}
const EVP_CIPHER* cipher = EVP_sm4_ecb();
```
3.初始化解密操作

```php {.line-numbers}
EVP_DecryptInit_ex(ctx, cipher, NULL, key, NULL);
```
4.解密

```php {.line-numbers}
long len;
EVP_DecryptUpdate(ctx, plaintext_decrypt, &len, ciphertext, ciphertext_len);
long plaintext_len = len;
EVP_DecryptFinal_ex(ctx, plaintext_decrypt + len, &len);
plaintext_len += len;
```
5.清理上下文

```php {.line-numbers}
EVP_CIPHER_CTX_free(ctx);
```
6.返回解密出的数据

# 运行效果
对于128bit的数据，加密用时0.001s，解密用时0s
![R{_IO}M8N$S A(UG@APSVZL](https://github.com/korangar-group42num1/group/assets/129478905/3653a6cf-0416-4234-a402-f59e96a2cf97)


