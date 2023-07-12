# 
基于RFC6979协议实现sm2
可以将RFC6979的简化版理解为：k = SHA256(d + HASH(m))
使用gmssl库中的sm2实现签名，k的选取参考RFC6979。

# 运行效果：
签名用时 0.005068063735961914 s
![image](https://github.com/korangar-group42num1/group42/assets/129478905/35279080-8fe7-466b-ac1b-7a679aad6d13)

# 参考文献：

1.https://zhuanlan.zhihu.com/p/55911409

2.https://www.cnblogs.com/pythonywy/p/13638806.html
