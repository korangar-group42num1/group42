from gmssl import sm3
import time
import random

def generate_random_str(randomlength=16):
  random_str =''
  base_str ='abcdefghigklmnopqrstuvwxyz0123456789'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str


def sm3_hash(msg):
    msg=bytearray(msg)
    h = sm3.sm3_hash(msg)
    return h

def rho(n):
    hash_list=[]
    hash_list_bit=[]
    msg=generate_random_str(64)
    

    while(1):
        if(len(hash_list)==0):
            hash_msg=sm3_hash(msg.encode())
        else:
            hash_msg=sm3_hash(hash_list[len(hash_list)-1].encode())
        
        if(hash_msg[0:n//4] in hash_list_bit):

            index=hash_list_bit.index(hash_msg[0:n//4])-1
            
            hash_list.append(hash_msg)
            hash_list_bit.append(hash_msg[0:n//4])
            
            print(n,"bits collision: ")
            print(hash_list[len(hash_list)-2],"and",hash_list[index])
            print(hash_list[len(hash_list)-2]," SM3 Hash: ",sm3_hash(hash_list[len(hash_list)-2].encode()))
            print(hash_list[index]," SM3 Hash: ",sm3_hash(hash_list[index].encode()))
            print("collision: ",hash_msg[0:n//4])
            return
        else:
            hash_list.append(hash_msg)
            hash_list_bit.append(hash_msg[0:n//4])
                        

i=4
i=int(i)
while(i<=40):
    start=time.time()
    rho(i)
    end=time.time()
    i+=4
    print("time: ",end-start," s\n")
