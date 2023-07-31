
iv =[0x7380166f,0x4914b2b9,0x172442d7,0xda8a0600,
     0xa96f30bc,0x163138aa,0xe38dee4d,0xb0fb0e4e]

t=[0x79cc4519,0x7a879d8a]

def left_move(x,j):
    j=j%32
    return ((x<<j)&0xffffffff)|((x&0xffffffff)>>(32-j))

def t_function(j):
    if(j>=0 and j<=15):
        return t[0]
    else:
        return t[1]

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
    a,b,c,d,e,f,g,h=v
    w,w_=message_extension(set_512,i)
    for j in range(0,64):
        ss1=left_move(left_move(a,12)+e+left_move(t_function(j),j),7)
        ss2=ss1^left_move(a,12)
        tt1=(ff(a,b,c,j)+d+ss2+w_[j])%(2**32)
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
def message_extension(set_512,i):
    w=[]
    w_=[]
    for j in range(0,16):
        w.append(int(set_512[i][8*j:8*(j+1)],16))
    for j in range(16,68):
        w.append(p1(w[j-16]^w[j-9]^left_move((w[j-3]),15))^left_move((w[j-13]),7)^w[j-6])
    for j in range(0,64):
        w_.append(w[j]^w[j+4])
            
    return w,w_


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


    
    





    
    
    




