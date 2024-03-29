from CryptoUtils import AESSIVDecryptNonce, AESSIVEncryptNonce, phiFunction, get_xor
from itertools import cycle
from BuildIndex import keyPhi

# Search over the search index I using the search token generated with
# algorithm Trapdoor
def Search(I, minecraftdoor):

    (A, T) = I # parse index
    (pos,Kw) = minecraftdoor[0] # parse trapdoor
    print('Searching:', pos)

    # for k,v in T.items():
    #     print(k,v)

    # Locate entry T[pos]
    theta = T[pos]
    # print('value:',theta)

    # Parse a||k = theta xor Kw
    (addr, k) = theta[0] #retrieve addr and k of node
    # print(addr)
    # print(k)
    Ki = phiFunction(keyPhi, pos) #get key Ki (pos=keyword)
    addr = bytes(addr ^ Ki for addr, Ki in zip(addr, cycle(Ki))) #addr xor Ki
    k = bytes(k ^ Ki for k, Ki in zip(k, cycle(Ki))) #k xor Ki
    print('retrieve addr:', addr)
    print('retrieve k:', k)

    # Decrypt linkedlist L with first node A[a] encrypted under key k
    # Decrypt all nodes from address
    print('decrypt addr (WIP)')
    # addressDegenerator = PsiCipher.decryptor()
    # decaddr = addressDegenerator.decrypt((1).to_bytes(16, "big"))
    # print(decaddr)

    # Output each decrypted record ID!
    result = 0
    return result # return encrypted records that match search criterion w


