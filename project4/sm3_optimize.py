import numpy as np
from numba import jit


def left_move(x,j):
    j=j%32
    return ((x<<j)&0xffffffff)|((x&0xffffffff)>>(32-j))

def ff(x,y,z,j):
    if(j>=0 and j<=15):
        return x^y^z
    else:
        return ((x&y)|(x&z)|(y&z))
    
def gg(x,y,z,j):
    if(j>=0 and j<=15):
        return x^y^z
    else:
        return ((x&y)|(~x&z))
      
def p0(x):
    return x^left_move(x,9)^left_move(x,17)

def p1(x):
    return x^left_move(x,15)^left_move(x,23)

def padding(msg):
    msg_bin=bin(int(msg,16))[2:]
    l=len(msg_bin)
    if(l%4!=0):
        for j in range(1,4):
            if (l+j)%4==0:
                msg_bin=j*'0'+msg_bin
    l=len(msg_bin)
    
    #padding 1
    msg_padding=msg_bin+'1'
    for k in range(0,512):
        if(l+1+k)%512==448:
            msg_padding=msg_padding+k*'0'
            break
        
    #padding 2
    l_bin='0'*(64-len(bin(l)[2:]))+bin(l)[2:]
    msg_padding=msg_padding+l_bin
    #print(msg_padding)
    msg_padding=hex(int(msg_padding,2))[2:]
    return msg_padding

def get_set(msg_padding):
    #分组
    set_512=[]
    n_set=len(msg_padding)//128
    for j in range(0,n_set):
        msg_512=msg_padding[128*j:128*(j+1)]
        set_512.append(msg_512)
    return set_512

def iterative_compression(set_512,iv_use):
    v=[]
    v.append(iv_use)
    n_set=len(set_512)
    for i in range(0,n_set):
        v.append(cf(v[i],set_512,i))
    return v[n_set]


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
    
    #optimize2   
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


def sm3(msg,iv_use):
    msg=msg.encode().hex()
    msg_padding=padding(msg)
    set_512=get_set(msg_padding)
    v_hash=iterative_compression(set_512,iv_use)
    sm3_hash=''
    for i in range(0,len(v_hash)):
        sm3_hash+=(8-len(hex(v_hash[i])[2:]))*'0'
        sm3_hash+=hex(v_hash[i])[2:]
    return sm3_hash


    
    





    
    
    




