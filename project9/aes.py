from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

key=b'1234567890123456'
iv=b'abcdefghijklmnop'
cipher=AES.new(key,AES.MODE_CBC,iv)

text=b'SDU2021Project9'
padtext=pad(text,16,style='pkcs7')
cipherText=cipher.encrypt(padtext)
print(padtext)
print(cipherText)

decrypter=AES.new(key,AES.MODE_CBC,iv)
plaintext=decrypter.decrypt(cipherText)
unpadtext=unpad(plaintext,16,'pkcs7')
print(plaintext)
print(unpadtext)
