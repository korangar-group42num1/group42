# 实验内容

*Project: Impl Merkle Tree following RFC6962

• Construct a Merkle tree with 10w leaf nodes

• Build inclusion proof for specified element

• Build exclusion proof for specified element


# 实验原理

## Merkle Tree

默克尔树（Merkle tree）是一种数据结构，以它的提出者默克尔命名，根据默克尔树的性质也可以叫哈希树，是一种典型的二叉树。

默克尔树由根，分支（中间的非叶节点），叶节点组成。

它具有以下重要的特点：
    1.Merkle Tree是一种树，大多数是二叉树，也可以多叉树，无论是几叉树，它都具有树结构的所有特点；
    
    2.Merkle Tree的叶子节点的value是数据集合的单元数据或者单元数据HASH。
    
    3.非叶子节点的value是根据它下面所有的叶子节点值，然后按照Hash算法计算而得出的。
    
![Merkle tree](https://github.com/korangar-group42num1/group/assets/129478905/eedda94e-07dd-455d-8a82-3270055fb121)

## Construct a Merkle Tree with RFC6962

       Logs use a binary Merkle Hash Tree for efficient auditing.  The
   hashing algorithm is SHA-256 [FIPS.180-4] (note that this is fixed
   for this experiment, but it is anticipated that each log would be
   able to specify a hash algorithm).  The input to the Merkle Tree Hash
   is a list of data entries; these entries will be hashed to form the
   leaves of the Merkle Hash Tree.  The output is a single 32-byte
   Merkle Tree Hash.  Given an ordered list of n inputs, D[n] = {d(0),
   d(1), ..., d(n-1)}, the Merkle Tree Hash (MTH) is thus defined as
   follows:

   The hash of an empty list is the hash of an empty string:

           MTH({}) = SHA-256().
   The hash of a list with one entry (also known as a leaf hash) is:
   
           MTH({d(0)}) = SHA-256(0x00 || d(0)).
   
   For n > 1, let k be the largest power of two smaller than n (i.e.,
   k < n <= 2k).  The Merkle Tree Hash of an n-element list D[n] is then
   defined recursively as
   
           MTH(D[n]) = SHA-256(0x01 || MTH(D[0:k]) || MTH(D[k:n])),

   where || is concatenation and D[k1:k2] denotes the list {d(k1),
   d(k1+1),..., d(k2-1)} of length (k2 - k1).  (Note that the hash
   calculations for leaves and nodes differ.  This domain separation is
   required to give second preimage resistance.)

   Note that we do not require the length of the input list to be a
   power of two.  The resulting Merkle Tree may thus not be balanced;
   however, its shape is uniquely determined by the number of leaves.
   (Note: This Merkle Tree is essentially the same as the history tree
   [CrosbyWallach] proposal, except our definition handles non-full
   trees differently.)

   ![Merkle Tree with RFC6962](https://github.com/korangar-group42num1/group/assets/129478905/42eed720-6c52-4aca-a307-f41bbe293a46)

## 代码实现

### Construct a Merkle tree with 10w leaf nodes

计算每个消息的哈希值

```php {.line-numbers} 
    for i in range(0,len(leaves)):
        leaf='0x00'+leaves[i]
        #print(leaf)
        hashed_leaf = sha256(leaf)
        tree_temp.append(hashed_leaf)
    tree.append(tree_temp)
```

构造哈希树

```php {.line-numbers} 
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
```
### Build inclusion proof for specified element

![inclusion proof](https://github.com/korangar-group42num1/group/assets/129478905/d3dae7c3-da2a-4a2b-acb0-a7d52140d80b)

要求在其他数据未送达之前，确认以下内容：
    1.消息1的确存在于这组数据中
    2.消息1的位置是第1位（从0开始计数）
则需要获取图中阴影部分的消息，逐步计算，最后与根节点对比，一致则说明消息真实且传输无误。

计算确认消息需要的节点，即消息的```哈希值的兄弟节点 ( brother node ) ```和```他们的父节点 ( father node ) 的兄弟节点```

```php {.line-numbers}
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

```

逐步计算验证消息

```php {.line-numbers}

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
```
### Build exclusion proof for specified element

证明过程中出现错误（如消息不存在或消息位置错误），同理。

```php {.line-numbers}

def exclusion_proof(msg,tree,site):
    if(inclusion_proof(msg,tree,site)==1):
        return 0
    else:
        return 1

```
## 运行效果

![Running effect](https://github.com/korangar-group42num1/group/assets/129478905/ea0dbda2-b254-4fdf-937a-cfaf1829b18d)

project|time
-|-
Construct a Merkle tree with 10w leaf nodes|0.18351221084594727 s
Build inclusion proof for specified element|0.027242183685302734 s
Build exclusion proof for specified element ( false meesage ) | 0.028707027435302734 s
Build exclusion proof for specified element ( false site ) |0.023746728897094727 s

# 参考资料

1.https://blog.csdn.net/wo541075754/article/details/54632929?ops_request_misc

2.https://www.rfc-editor.org/rfc/rfc6962#section-2.1.2

3.https://ethbook.abyteahead.com/ch4/merkle.html 
