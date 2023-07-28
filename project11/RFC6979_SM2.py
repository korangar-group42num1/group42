from gmssl import sm2
import hashlib
import time

def gen_k(privateKey, data):
    # Converts a string to an array of bytes
    privateKey_bytes = privateKey.encode('utf-8')
    #data_bytes = data.encode('utf-8')

    # Compute HASH(data)
    hash_data = hashlib.sha256(data).digest()

    # Concatenate the string d with HASH(m) to calculate SHA256
    concatenated_bytes = privateKey_bytes + hash_data
    k = hashlib.sha256(concatenated_bytes).hexdigest()

    return k

#Public key,private ke,data
private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
data = b"SDU2021Project11"

start=time.time()
sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
k=gen_k(private_key,data)
sign = sm2_crypt.sign(data, k) 
end=time.time()

assert sm2_crypt.verify(sign, data)

print("data :",data,"\n")
print("k :",k,"\n")
print("signature :",sign,"\n")
print("time :",end-start,"s")
