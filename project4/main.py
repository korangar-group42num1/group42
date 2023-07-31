import sm3
import sm3_optimize
import time
import random

iv =[0x7380166f,0x4914b2b9,0x172442d7,0xda8a0600,
     0xa96f30bc,0x163138aa,0xe38dee4d,0xb0fb0e4e]

t=[0x79cc4519,0x7a879d8a]

def generate_random_str(randomlength=16):
  """
  生成一个指定长度的随机字符串
  """
  random_str =''
  base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str

    
message=generate_random_str(100000)
start=time.time()
hash_message=sm3.sm3(message,iv)
end=time.time()

print("before optimizing:")
print("time:",end-start,"s")

start=time.time()
hash_message_optimize=sm3_optimize.sm3(message,iv)
end=time.time()

assert hash_message==hash_message_optimize

print("after optimizing:")
print("time:",end-start,"s")





