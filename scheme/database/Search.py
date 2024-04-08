from itertools import cycle
import os
from utils.CryptoUtils import AESSIVDecryptNonce
from utils.CryptoUtils import xor
from utils.Node import Node
# Search over the search index I using the search token generated with
# algorithm Trapdoor
def Search(I, minecraftdoor):

    (A, T) = I # parse index into A array and T lookup table
    (pos,Kw) = minecraftdoor # parse trapdoor

    # Locate entry T[pos]
    print('lookup node address at pos [',str(pos),'] in table T')
    try:
        theta = T[str(pos)]
    except:
        return []
    # Parse a||k = theta xor Kw (for each node)
    node = theta[0]
    (addr, kHead) = node #retrieve addr and k of node
    nextAddr = int.from_bytes(xor(addr, Kw), 'big')
    print('get node address [',addr,'] and xor')
    print('locating node at address [',nextAddr,'] in A')
    nextKey = xor(kHead, Kw)

    results = []

    while(nextAddr is not None):
        try:
            N = A[nextAddr]
        except:
            print("Address not found!!!!")
            return results
        
        node = AESSIVDecryptNonce(nextKey, N)
        curNode = Node.parseString(str(node.decode()))
        results.append(curNode.recordID)
        print('hit! [',curNode.recordID,'] at node address [',nextAddr,']')
        nextAddr = curNode.addressNext
        nextKey = curNode.kNext

    return results # return encrypted records that match search criterion w


