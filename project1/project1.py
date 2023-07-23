from gmssl import sm3
import time
import random

# 计算SM3哈希值
def sm3_hash(msg):
    msg=bytearray(msg)
    h = sm3.sm3_hash(msg)
    return h

        
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


#寻找碰撞
def get_collision(n):
    str_list=[]
    index=-1
    index=int(index)
    while(index<int(1.177*pow(2,n//2))):
        index+=1
        rand_i=generate_random_str(random.randint(1,100))
        if(rand_i in str_list):
            index-=1
            continue
        str_list.append(rand_i)
    for i in range(0,int(1.177*pow(2,n//2))):
        str_list_i=str_list[i]
        hash_i=sm3_hash(str_list_i.encode())
        for j in range(i+1,int(1.177*pow(2,n//2))):
            str_list_j=str_list[j]
            hash_j=sm3_hash(str_list_j.encode())
            for k in range(0,n//4):
                if(hash_i[k]!=hash_j[k]):
                    break
                if(k==n//4-1):
                    print(n," bits collision:")
                    print(str_list_i," and ",str_list_j)
                    print(str_list_i," sm3 hash: ",hash_i)
                    print(str_list_j," sm3 hash: ",hash_j)
                    print("collision : ",end="")
                    for bit in range(0,n//4):
                        print(hash_i[bit],end="")
                    print("\n")
                    return 1
    print(n,"bits not found\n")
    return 0

i=4
count=0
count_sucess=0
time_all=0;
time_all=float(time_all)
i=int(i)
for k in range(0,100):
    print("—————————— ",k," ——————————\n")
    while(i<17):
        count+=1
        start=time.time()
        if(get_collision(i)==1):
            count_sucess+=1
        end=time.time()
        time_all+=(end-start)
        i=i+4
        print("time : ",end-start," s\n")
    i=4
print("the rate: ",100*(count_sucess/count),"%\n")
print("all time: ",time_all," s\n")

    



            
                    
            
    






