import hashlib
import random
import time

def sha256(msg):    
    msg_hash=hashlib.sha256(msg.encode()).hexdigest()
    return msg_hash
    
def generate_random_str(randomlength=16):
    random_str =''
    base_str ='abcdefghigklmnopqrstuvwxyz0123456789'
    length =len(base_str) -1
    for i in range(randomlength):
        random_str +=base_str[random.randint(0, length)]
    return random_str


def construct_merkle_tree(leaves):
    if len(leaves) == 0:
        raise ValueError("No leaves provided")
    #print(leaves)
    tree = []
    tree_temp=[]
    for i in range(0,len(leaves)):
        leaf='0x00'+leaves[i]
        #print(leaf)
        hashed_leaf = sha256(leaf)
        tree_temp.append(hashed_leaf)
    tree.append(tree_temp)
    
    len_tree_temp=len(tree[0]) # number of nodes in a layer
    
    while (len_tree_temp > 1):
        tree_temp = []
        #print(tree)
        for i in range(0, len_tree_temp-1, 2):
            concat_hashes = '0x01'+tree[len(tree)-1][i] + tree[len(tree)-1][i+1]
            #print(concat_hashes)
            parent_hash = sha256(concat_hashes)
            tree_temp.append(parent_hash)
        if(len_tree_temp%2!=0):
            tree_temp.append(tree[len(tree)-1][len_tree_temp-1])
        tree.append(tree_temp)
        len_tree_temp=len(tree_temp)

    return tree

def inclusion_proof(msg,tree,site):
    print("message:",msg)
    msg_hash=sha256('0x00'+msg)
    hash_list_verify=[]
    hash_list_left=[]
    
    #print(len(tree)-1)
    
    for i in range(0,len(tree)-1):
        if(site%2==0):
            brother_site=site+1
            father_site=site//2
            left_brother=0
        else:
            brother_site=site-1
            father_site=(site-1)//2
            left_brother=1
            
        #add a brother node to the list, turn itself into a father node, and then look for it
        hash_list_verify.append(tree[i][brother_site])
        hash_list_left.append(left_brother)
        site=father_site

    #verify
    final_node=tree[len(tree)-1][0]
    node_temp=msg_hash
    for i in range(0,len(hash_list_verify)):
        if(hash_list_left[i]==1):
            node_temp=sha256('0x01'+hash_list_verify[i]+node_temp)
        else:
            node_temp=sha256('0x01'+node_temp+hash_list_verify[i])
            
    #print(hash_list_verify)
    
    if(node_temp==final_node):
        print("This message exists and is in the correct location!")
        return 1
    else:
        #print(2)
        print("Something went wrong!")
        return 0
    
        
   
def exclusion_proof(msg,tree,site):
    if(inclusion_proof(msg,tree,site)==1):
        return 0
    else:
        return 1
    

leaves_list=[]
len_leaves=100000
msg_right_site=random.randint(0,len_leaves-1)
msg_false=generate_random_str(60)
msg_false_site=msg_right_site+1
for i in range(0,len_leaves): 
    leaves_list.append(generate_random_str(50))

start=time.time()
tree=construct_merkle_tree(leaves_list)
end=time.time()
print("Time of constructing a Merkle tree with",len_leaves,"leaf nodes: ",end-start,"s\n")

start=time.time()
inclusion_proof(leaves_list[msg_right_site],tree,msg_right_site)
end=time.time()
print("Time of building inclusion proof for specified element: ",end-start,"s\n")


start=time.time()
exclusion_proof(msg_false,tree,msg_right_site)
end=time.time()
print("Time of building inclusion proof for specified element: ",end-start,"s\n")

start=time.time()
exclusion_proof(leaves_list[msg_right_site],tree,msg_false_site)
end=time.time()
print("Time of building inclusion proof for specified element: ",end-start,"s\n")
