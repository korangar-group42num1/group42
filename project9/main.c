#include<stdio.h>
#include <time.h>

int main(void) {
	//long plaintext[4]; // 明文
	unsigned long rowkey[32]; // 轮密钥
	unsigned long K[4]; // 中间数据
	long plaintext[4];
	unsigned long ciphertext[4]; // 密文
	unsigned long key[] = { 0x01122334,0x45566778,0x899aabbc,0xcddeeff0 };
	unsigned long plaintext_all[] = { 0x01122334,0x45566778,0x899aabbc,0xcddeeff0};
    long plaintext_len = sizeof(plaintext_all) / sizeof(plaintext_all[0]);
	Keyextend(key, K, rowkey);
	printf("plaintext：\n");
	for (long i = 0; i < plaintext_len; i += 4) {
		printf("%08x %08x %08x %08x\n", plaintext_all[0], plaintext_all[1], plaintext_all[2], plaintext_all[3]);
	}
	
	printf("\nciphertext：\n");
	for(long i=0;i<plaintext_len;i+=4){
		plaintext[0]=plaintext_all[i];
		plaintext[1]=plaintext_all[i+1];
		plaintext[2]=plaintext_all[i+2];
		plaintext[3]=plaintext_all[i+3];
		encryptSM4(plaintext, rowkey ,ciphertext) ;
		printf("%08x %08x %08x %08x\n", ciphertext[0], ciphertext[1], ciphertext[2], ciphertext[3]);
	}
	
    return 0;
}
