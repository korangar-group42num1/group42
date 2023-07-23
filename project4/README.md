# 实验内容

**Project4: do your best to optimize SM3 implementation (software)**

# 实验原理

## 优化一：预计算常数（查表优化）

预先计算并存储常数 **ti=Ti<<<i**，存储到表中，则 **left_t=t[i]**

这可以避免每个消息分组都去计算常数，且占用的存储空间也很少，仅256 Byte


## 优化二：消息扩展的快速实现

消息扩展的目的是利用512比特的消息分组B扩展得到68个字W0,…,W67和64个字W′0,…,W′63。

快速实现时，为了尽可能减少不必要的数据加载和存储，W0,…,W67和W′0,…,W′63的计算可以调整到压缩函数里执行，具体实施过程是：

```
1)首先在执行12-64轮压缩函数前计算初始的4个字W0,…,W15；

2)然后在压缩函数的12-64轮的第i轮生成Wi+4，而W′i则使用W′i=Wi⊕Wi+4代替。
```

经过这样的调整，去掉了字W′0,…,W′63，减少了字W0,…,W67和W′0,…,W′63的加载和存储次数，提高了消息扩展的速度。


## 优化三：numpy(simd)

在数组操作时使用**numpy**库，**numpy**背后使用的是**simd指令**，即通过并行提高速度。

## 代码实现

### 运行指导

将三个文件：sm3.py，sm3_optimize.py,test.py添加到同一目录下，可直接运行

### 关键代码

```php {.line-numbers}

def cf(v,set_512,i):
    #optimize1
    left_t=[2043430169,4086860338,3878753381,3462539467, 
        2630111639,965255983,1930511966,3861023932, 
        3427080569,2559193843,823420391,1646840782, 
        3293681564,2292395833,289824371,579648742, 
        2643098247,991229199,1982458398,3964916796, 
        3634866297,2974765299,1654563303,3309126606, 
        2323285917,351604539,703209078,1406418156, 
        2812836312,1330705329,2661410658,1027854021, 
        2055708042,4111416084,3927864873,3560762451, 
        2826557607,1358147919,2716295838,1137624381, 
        2275248762,255530229,511060458,1022120916, 
        2044241832,4088483664,3882000033,3469032771, 
        2643098247,991229199,1982458398,3964916796, 
        3634866297,2974765299,1654563303,3309126606, 
        2323285917,351604539,703209078,1406418156, 
        2812836312,1330705329,2661410658,1027854021]
    a,b,c,d,e,f,g,h=v
    
    #optimize2+3  
    w = np.array=[int(set_512[i][0:8],16),int(set_512[i][8:16],16),
                  int(set_512[i][16:24],16),int(set_512[i][24:32],16),
                  int(set_512[i][32:40],16),int(set_512[i][40:48],16),
                  int(set_512[i][48:56],16),int(set_512[i][56:64],16),
                  int(set_512[i][64:72],16),int(set_512[i][72:80],16),
                  int(set_512[i][80:88],16),int(set_512[i][88:96],16),
                  int(set_512[i][96:104],16),int(set_512[i][104:112],16),
                  int(set_512[i][112:120],16),int(set_512[i][120:128],16)]
    for j in range(0,12):           
        ss1=left_move(left_move(a,12)+e+left_t[j],7)
        ss2=ss1^left_move(a,12)
        tt1=(ff(a,b,c,j)+d+ss2+(w[j]^w[j+4]))%(2**32)
        tt2=(gg(e,f,g,j)+h+ss1+w[j])%(2**32)
        d=c
        c=left_move(b,9)
        b=a
        a=tt1
        h=g
        g=left_move(f,19)
        f=e
        e=p0(tt2)

    for j in range(12,64):
        w.append(p1(w[j+4-16]^w[j+4-9]^left_move((w[j+4-3]),15))
                 ^left_move((w[j+4-13]),7)^w[j+4-6])
        ss1=left_move(left_move(a,12)+e+left_t[j],7)
        ss2=ss1^left_move(a,12)
        tt1=(ff(a,b,c,j)+d+ss2+(w[j]^w[j+4]))%(2**32)
        tt2=(gg(e,f,g,j)+h+ss1+w[j])%(2**32)
        d=c
        c=left_move(b,9)
        b=a
        a=tt1
        h=g
        g=left_move(f,19)
        f=e
        e=p0(tt2)
        
    a_,b_,c_,d_,e_,f_,g_,h_=v
    
    return a_^a,b_^b,c_^c,d_^d,e_^e,f_^f,g_^g,h_^h

```

# 运行效果

分别测试对于80000 bits,800000 bits,8000000 bits,80000000 bits的运行速度

![image](https://github.com/korangar-group42num1/group/assets/129478905/15f60a04-1631-43dc-80d2-5d2c1e1cb001)

bit|time(before)|time(after)
-|-|-
80000|0.03400778770446777 s|0.032007694244384766 s
800000|0.3421816825866699 s|0.3281223773956299 s
8000000|3.4120867252349854 s|3.2406201362609863 s
80000000|35.347118616104126 s|33.3248074054718 s

#参考资料

1.http://www.sca.gov.cn/sca/xwdt/2010-12/17/1002389/files/302a3ada057c4a73830536d03e683110.pdf

2.https://kns.cnki.net/kcms2/article/abstract?v=3uoqIhG8C44YLTlOAiTRKibYlV5Vjs7ijP0rjQD-AVm8oHBO0FTadhAv7PwoTU6RpNwhQEDr8LlG91k5pQNnPnZ--I5ZBTJl&uniplatform=NZKPT







