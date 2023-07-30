import sm3
import random
import time

iv =[0x7380166f,0x4914b2b9,0x172442d7,0xda8a0600,
     0xa96f30bc,0x163138aa,0xe38dee4d,0xb0fb0e4e]

def generate_random_str(randomlength=16):   
    random_str =''
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length =len(base_str) -1
    for i in range(randomlength):
      random_str +=base_str[random.randint(0, length)]
    return random_str

def length_extension_attack(msg_hash,msg_ext):
    iv_new=[]
    for i in range(0,8):
        iv_new.append(int(msg_hash[8*i:8*(i+1)],16))        
    msg_ext_hash=sm3.sm3(msg_ext,iv_new)
    return msg_ext_hash

def verify_length_extension_attack(msg,ext):
    msg_padding=sm3.padding(message.encode().hex())
    ext_padding=sm3.padding(ext.encode().hex())
    set_512=sm3.get_set(msg_padding+ext_padding)
    v_hash=sm3.iterative_compression(set_512,iv)
    sm3_hash=''
    for i in range(0,len(v_hash)):
        sm3_hash+=(8-len(hex(v_hash[i])[2:]))*'0'
        sm3_hash+=hex(v_hash[i])[2:]
    return sm3_hash

num_bit=1000*8
message=generate_random_str(num_bit//8)
ext='SDU_2021_Project3'*10+'length_extension_attack'*10
msg_hash=sm3.sm3(message,iv)
start=time.time()
hash1=length_extension_attack(msg_hash,ext)
hash2=verify_length_extension_attack(message,ext)
end=time.time()

print("length of message:",num_bit,"bits")
print("length of extended message:",len(ext)*8,"bits")
if(hash1==hash2):
    print("Successful attack!")
    print("hash(message_padding||extent_padding):",hash1)
    print("time: ",end-start,"s")
else:
    print("Attack failure!")
    




