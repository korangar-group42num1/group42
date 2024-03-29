# 实验原理
## Rho methon

    以上一个哈希值作为下一个哈希值的原像，不断计算下去。消息的个数是有限的，所以最终一定在某处重合，即构成环形。
    
![image](https://github.com/korangar-group42num1/group42/assets/129478905/6e8bd277-c3be-4f5a-b060-d4f82296657d)


## 实验思路

    1.首先生成一个随机消息msg，计算其SM3哈希值hash1=hash(msg)
    
    2.以上一步计算出的哈希值为原像，计算hash1的哈希值hash2=hash(hash1)
    
    3.以此类推，不断循环计算知道出现前n比特发生碰撞

## 关键代码

```python
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
```

# 运行效果（攻击至 40 bits）

Rho methon受**随机性**影响，决定攻击时间的因素是最初随机生成的数据，攻击事件波动较大。此数据仅为单次运行结果。
## 1
![image](https://github.com/korangar-group42num1/group42/assets/129478905/5e11a134-b69d-42a8-8ddf-6d4eb12fe66e)
![image](https://github.com/korangar-group42num1/group42/assets/129478905/60f1f67e-3439-4e18-9962-b71a9de8d27f)

## 2
![image](https://github.com/korangar-group42num1/group/assets/129478905/f728f7d6-a87d-4961-8574-c3c0fc03f38e)
![image](https://github.com/korangar-group42num1/group/assets/129478905/7021cfc8-b74b-46b4-a1ec-63a39285a290)

## 3
![image](https://github.com/korangar-group42num1/group/assets/129478905/82ec532f-a1a7-4a39-bab1-3f5ee411dfa9)
![image](https://github.com/korangar-group42num1/group/assets/129478905/98d1782a-b877-4644-bdbd-c41d0f0ac7f1)

如图，**时间波动较大**

bit|time1|time2|time3
-|-|-|-
4|0.059868574142456055 s|0.12188506126403809 s|0.12612295150756836 s
8|0.06680941581726074 s|0.1397860050201416 s|0.1378166675567627 s
12|0.08911871910095215 s|0.18645071983337402 s|0.202911376953125 s
16|0.35831785202026367 s|0.49365973472595215 s|0.5124292373657227 s
20|2.2606167793273926 s|0.8372244834899902 s|2.1720094680786133 s
24|4.640185356140137 s|9.30874252319336 s|0.7790565490722656 s
28|30.09235906600952 s|23.06446361541748 s|34.35939121246338 s
32|72.7560408115387 s|304.230838060379 s|169.6727693080902 s
36|123.46740221977234 s|514.4690353870392 s|86.02591753005981 s
40|13343.946993350983 s|18143.982656002045 s|11099.375796794891 s
    
