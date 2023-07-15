# 实验原理
## Rho methon

    以上一个哈希值作为下一个哈希值的原像，不断计算下去。消息的个数是有限的，所以最终一定在某处重合，即构成环形。
    
![image](https://github.com/korangar-group42num1/group42/assets/129478905/6e8bd277-c3be-4f5a-b060-d4f82296657d)


## 实验思路

    1.首先生成一个随机消息msg，计算其SM3哈希值hash1=hash(msg)
    2.以上一步计算出的哈希值为原像，计算hash1的哈希值hash2=hash(hash1)
    3.以此类推，不断循环计算知道出现前n比特发生碰撞

# 运行效果

Rho methon受`随机性`影响，攻击事件波动较大。此数据仅为单次运行结果。

![image](https://github.com/korangar-group42num1/group42/assets/129478905/5e11a134-b69d-42a8-8ddf-6d4eb12fe66e)
![image](https://github.com/korangar-group42num1/group42/assets/129478905/60f1f67e-3439-4e18-9962-b71a9de8d27f)

bit|time
-|-
4|0.059868574142456055 s
8|0.06680941581726074 s
12|0.08911871910095215 s
16|0.35831785202026367 s
20|2.2606167793273926 s
24|4.640185356140137 s
28|30.09235906600952 s
32|72.7560408115387 s
36|123.46740221977234 s
40|13343.946993350983 s

    
