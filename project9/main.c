#include <openssl/evp.h>
#include <string.h>
#include<stdio.h>
#include <time.h>
int main() {
    unsigned char plaintext[] = { 0x01,0x12,0x23,0x34,
                              0x45,0x56,0x67,0x78,
                              0x89,0x9A,0xAB,0xBC,
                              0xCD,0xDE,0xEF,0xF0 };

    unsigned char key[] = { 0x01,0x12,0x23,0x34,
                              0x45,0x56,0x67,0x78,
                              0x89,0x9A,0xAB,0xBC,
                              0xCD,0xDE,0xEF,0xF0 };
    unsigned char ciphertext[10240];
    unsigned char plaintext_decrypt[10240];
    long plaintext_len = sizeof(plaintext) / sizeof(plaintext[0]);
    clock_t start, end;
    start = clock();
    long ciphertext_len = encrypt(plaintext, key, ciphertext, plaintext_len);
    end = clock();
    printf("Ciphertext: ");
    for (long i = 0; i < ciphertext_len; i++) {
        printf("%02X", ciphertext[i]);
        printf(" ");
    }
    printf("\n加密时间为%fs\n", ((double)(end - start)) / CLOCKS_PER_SEC);

    start = clock();
    plaintext_len = decrypt(plaintext_decrypt, key, ciphertext, ciphertext_len);
    end = clock();
    printf("Plaintext: ");
    for (long i = 0; i < plaintext_len; i++) {
        printf("%02X", plaintext_decrypt[i]);
        printf(" ");
    }
    printf("\n解密时间为%fs\n", ((double)(end - start)) / CLOCKS_PER_SEC);
    return 0;
}
