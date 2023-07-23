#include <openssl/evp.h>
#include <string.h>
#include<stdio.h>
#include <time.h>

long encrypt(unsigned char plaintext[], unsigned char key[], unsigned char ciphertext[],long plaintext_len) {
    //������
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX_init(ctx);

    //����ģʽ
    const EVP_CIPHER* cipher = EVP_sm4_ecb();

    // ��ʼ�����ܲ���
    EVP_EncryptInit_ex(ctx, cipher, NULL, key, NULL);

    //����    
    long len;
    EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len);
    long ciphertext_len = len;
    EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
    ciphertext_len += len;

    // ����������
    EVP_CIPHER_CTX_free(ctx);
    return  ciphertext_len;

}
long decrypt(unsigned char plaintext_decrypt[], unsigned char key[], unsigned char ciphertext[],
             long ciphertext_len)
{
    //������
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX_init(ctx);

    //����ģʽ
    const EVP_CIPHER* cipher = EVP_sm4_ecb();

    // ��ʼ�����ܲ���
    EVP_DecryptInit_ex(ctx, cipher, NULL, key, NULL);

    // ����
    long len;
    EVP_DecryptUpdate(ctx, plaintext_decrypt, &len, ciphertext, ciphertext_len);
    long plaintext_len = len;
    EVP_DecryptFinal_ex(ctx, plaintext_decrypt + len, &len);
    plaintext_len += len;

    // ����������
    EVP_CIPHER_CTX_free(ctx);
    return plaintext_len;
}

