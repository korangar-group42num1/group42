# 实验内容

**Project9: AES / SM4 software implementation**

两种实现方式：

**不调用openssl库**

**调用openssl库**

# 不调用openssl库

## 运行指导

将文件 **sm4.c** 和 **main.c** 添加到同一项目内，可直接运行

## 实验原理

### 查找S盒

```php
unsigned long findinsbox(unsigned long b) {
	unsigned char a[4];
	
	a[0] = b / 0x1000000;//16**6
	a[1] = b / 0x10000;//16**4
	a[2] = b / 0x100;//16**2=256
	a[3] = b;
	b = Sbox[a[0]] * 0x1000000 + Sbox[a[1]] * 0x10000 + Sbox[a[2]] * 0x100 + Sbox[a[3]];
	return b;
}
```

### 循环左移

```php
long loopLeft(long a, int length) {
	
	for (int i = 0; i < length; i++) {
		a = a * 2 + a / 0x80000000;
	}
	return a;
}
```

### 线性变换函数L
```php
long functionL1(long a) {
	return a ^ loopLeft(a, 2) ^ loopLeft(a, 10) ^ loopLeft(a, 18) ^ loopLeft(a, 24);
}

long functionL2(long a) {
	return a ^ loopLeft(a, 13) ^ loopLeft(a, 23);
}
```

### 合成变换T

```php
//加密用T1，解密用T2
long T1(long a) {
	return functionL1(findinsbox(a)) ;
}
long T2(long a) {
	return  functionL2(findinsbox(a));
}
```

### 密钥拓展
```php
void Keyextend(long MK[],long K[],long RK[]) {
	
	for (int i = 0; i < 4; i++) {
		K[i] = MK[i] ^ FK[i];
	}
	for (int j = 0; j < 32; j++) {
		K[(j + 4) % 4] = K[j % 4] ^ T2(K[(j + 1) % 4] ^ K[(j + 2) % 4] ^ K[(j + 3) % 4] ^ CK[j]);
		RK[j] = K[(j + 4) % 4];
	}
}
```

### 加密算法

```php
void encryptSM4(long X[], long RK[] , long Y[]) {
	for (int i = 0; i < 32; i++) {
		X[(i + 4) % 4] = X[i % 4] ^ T1(X[(i + 1) % 4] ^ X[(i + 2) % 4] ^ X[(i + 3) % 4] ^ RK[i]);
	}
	for (int j = 0; j < 4; j++) {
		Y[j] = X[3 - j];
	}
}
```

### 解密算法

```php
void decryptSM4(long X[], long RK[], long Y[]) {

	long RKinvert[32];
	for (int i = 0; i < 32; i++) {
		RKinvert[i] = RK[31 - i];
	}
	encryptSM4(X, RKinvert, Y);

}
```

## 运行效果

![(CJ%~0DL{TUGIKORA7USRY0](https://github.com/korangar-group42num1/group/assets/129478905/dac49796-1f54-4e55-b114-5d0171b6f339)


# 调用openssl库

## 运行指导

1.安装开源库openssl并配置在vs中

2.将文件 **sm4_openssl.c** 和 **main_openssl.c** 添加到同一项目内，可直接运行
  
## 实验原理

运用开源库**openssl**实现SM4的软件实现（ecb模式）

### 加密 long encrypt

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

### 解密 long decrypt

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

## 运行效果

![C@)Q 6FV K4BLZ5J`5`ARPC](https://github.com/korangar-group42num1/group/assets/129478905/a624dd84-4e5e-4aaa-826e-4b78ee8c9942)



