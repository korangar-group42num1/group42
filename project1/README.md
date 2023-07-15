# 实验原理
## 生日攻击
    对于n-bit的Hash函数（N=2^n），只要准备t≈1.177sqrt(2^n)个消息，就能以至少p=1/2的概率成功找到一对碰撞。

## 实验思路
    1.随机生成1.177sqrt(2^n)个消息
    2.计算1.177sqrt(2^n)个消息的sm3哈希值，存入数组中
    3.穷举表中元素查找碰撞
    4.选取多组消息（较小比特），测试攻击成功的比例
    5.单独测试对于较大比特的攻击

# 运行效果

各组成功概率约等于50%，符合生日攻击原理。

## 100组
运行时间：8.576 s

成功概率：45.25 %

![D}AJMM)4ADOT~E5K~6`L0RU](https://github.com/korangar-group42num1/group42/assets/129478905/86e5c67a-da69-40b7-8282-26988499ee7e)


## 200组
运行时间：17.608 s

成功概率：46.5 %

![C%3Y $BT7 XF`I9DCLN%`RL](https://github.com/korangar-group42num1/group42/assets/129478905/5b63e16d-6708-4ab4-80ba-91300d7acdc5)

## 500组
运行时间：54.656 s

成功概率：46.5 %

![QDK@3D53CIXF600%A13~P8W](https://github.com/korangar-group42num1/group42/assets/129478905/46bd242c-1113-4064-b855-ccc2b1ff17c7)

## 800组
运行时间：73.325 %

成功概率：44.5312 %

![USKD L9 E(E5V~IB69~HA9](https://github.com/korangar-group42num1/group42/assets/129478905/e6931b9c-2f26-472c-b373-31f287db1c3d)

## 1200组
运行时间：125.504 s

成功概率：43.8542 %

![I}7`}_3)LX2 316T FSYMWI](https://github.com/korangar-group42num1/group42/assets/129478905/26badbeb-6a03-4368-9725-9f33bfcc3cfd)

## 大比特攻击
1.
![image](https://github.com/korangar-group42num1/group42/assets/129478905/55b3f483-d5b3-4265-915d-d61f6cf98872)

2.
![20230715232747](https://github.com/korangar-group42num1/group42/assets/129478905/71da0063-8e70-408e-81c3-e47b1c8bfa33)


## 各长度攻击时间
注：受`消息的随机性`、`成功概率`、`输出所需时间`等因素的影响，控制台显示的单个时间仅为参考，需要'综合多次测试'得出时间。
bit|time
-|-
4 bits|< 0.01 s
8 bits|< 0.01 s
12 bits|≈ 0.015 s
16 bits|≈ 0.03 s
20 bits|≈ 0.04 s
24 bits|0.8 s —— 16 s
28 bits|1 s —— 30 s
32 bits|1000 s —— 4000 s



# 参考资料
    1.https://www.bilibili.com/read/cv14571497 
    2.https://blog.csdn.net/superfjj/article/details/117729922?ops_request_misc
    3.https://blog.csdn.net/zhizhengguan/article/details/106015398?ops_request_misc


