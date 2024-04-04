from itertools import cycle
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
import os

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
    for node in theta:
        (addr, k) = node #retrieve addr and k of node
        # print(addr)
        # print(k)

        # T[pos] (theta split into addr and k) xor Kw
        # print(type(addr), type(Kw))
        addr = bytes(addr ^ Kw for addr, Kw in zip(addr, cycle(Kw))) #addr xor Kw
        k = bytes(k ^ Kw for k, Kw in zip(k, cycle(Kw))) #k xor Kw
        # print('retrieve addr:', addr)
        # print('real address:', int.from_bytes(addr,'big'))
        # print('retrieve k:', k)

        # Decrypt linkedlist L with first node A[a] encrypted under key k
        # Decrypt all nodes from address
        aessiv = AESSIV(k) #decrypting each node with non deterministic encryptor
        ct = A[int.from_bytes(addr, 'big')] # retrieve ct
        # print('encrypted node:', ct)
        node = aessiv.decrypt(ct, None)
        print('decrypted node:',node.decode().split(' '))

        R.append(node.decode().split(' ')[0]) # add record id to list

    return R # return encrypted records that match search criterion w


