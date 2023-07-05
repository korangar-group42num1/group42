#include <openssl/evp.h>
#include <string.h>
#include<stdio.h>
#include <time.h>

long encrypt(unsigned char plaintext[], unsigned char key[], unsigned char ciphertext[],long plaintext_len) {
    //上下文
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX_init(ctx);

    //工作模式
    const EVP_CIPHER* cipher = EVP_sm4_ecb();

    // 初始化加密操作
    EVP_EncryptInit_ex(ctx, cipher, NULL, key, NULL);

    //加密    
    long len;
    EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len);
    long ciphertext_len = len;
    EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
    ciphertext_len += len;

    // 清理上下文
    EVP_CIPHER_CTX_free(ctx);
    return  ciphertext_len;

}
long decrypt(unsigned char plaintext_decrypt[], unsigned char key[], unsigned char ciphertext[],
             long ciphertext_len)
{
    //上下文
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX_init(ctx);

    //工作模式
    const EVP_CIPHER* cipher = EVP_sm4_ecb();

    // 初始化解密操作
    EVP_DecryptInit_ex(ctx, cipher, NULL, key, NULL);

    // 解密
    long len;
    EVP_DecryptUpdate(ctx, plaintext_decrypt, &len, ciphertext, ciphertext_len);
    long plaintext_len = len;
    EVP_DecryptFinal_ex(ctx, plaintext_decrypt + len, &len);
    plaintext_len += len;

    // 清理上下文
    EVP_CIPHER_CTX_free(ctx);
    return plaintext_len;
}
