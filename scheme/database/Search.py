from itertools import cycle
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
import os
from utils.CryptoUtils import xor
from utils.Node import Node
# Search over the search index I using the search token generated with
# algorithm Trapdoor
def Search(I, minecraftdoor):

    (A, T) = I # parse index
    (pos,Kw) = minecraftdoor[0] # parse trapdoor
    print('Searching:', pos)

    # for k,v in T.items():
    #     print(k,v)

    # Locate entry T[pos]
    theta = T[str(pos)]
    # print('value:',theta)

    R = [] # keeping track of record ids

    # Parse a||k = theta xor Kw (for each node)
    node = theta[0]
    (addr, kHead) = node #retrieve addr and k of node
    nextAddr = int.from_bytes(xor(addr, Kw), 'big')
    nextKey = xor(kHead, Kw)

    results = []

    while(nextAddr is not None):
        aessiv = AESSIV(nextKey) #decrypting each node with non deterministic encryptor
        try:
            N = A[nextAddr]
        except:
            print("Address not found!!!!")
            return results
        
        node = aessiv.decrypt(N, None)
        curNode = Node.parseString(str(node.decode()))
        results.append(curNode.recordID)
        nextAddr = curNode.addressNext
        nextKey = curNode.kNext

    return results # return encrypted records that match search criterion w


