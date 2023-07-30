import hashlib
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from gmssl import sm2
import time

def PGP(data):

    #会话密钥
    session_key = get_random_bytes(16)
    
    #aes加密消息
    #压缩消息
    hash_data = hashlib.sha256(data).digest()
    
    #aes对称加密
    iv = get_random_bytes(16)
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    ciphertext_aes = cipher.encrypt(pad(hash_data, AES.block_size))

    #sm2加密会话密钥
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    ciphertext_sm2 = sm2_crypt.encrypt(session_key)

    #拼合并转为文本数据
    ciphertext=(ciphertext_sm2+ciphertext_aes).hex().encode('utf-8')

    return ciphertext

data=b'SDU2021Project14'
start=time.time()
pgp_data=PGP(data)
end=time.time()
print("enc_data:\n",pgp_data,"\n")
print("time:\n",end-start,"s")

