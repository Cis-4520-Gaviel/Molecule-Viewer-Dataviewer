import os
from utils.Node import Node
from utils.AESCTR import AESCTR
from cuckoopy import CuckooFilter
from utils.CryptoUtils import AESSIVDecryptNonce, AESSIVEncryptNonce, phiFunction
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
from users.CreateDictionary import GetKeyAtValue
from itertools import cycle
from pymcl import pairing, g1, g2, Fr

# Generate a search index I
def BuildIndex(W: dict, n: int, K: tuple, Klen: int, secretKey: Fr, debugDetailed = False):
    """
    Builds an encrypted index to allow searching over an encrypted database Name='Fire'

    Params: W - a dictionary of keywords, each mapping to an array of records which contain keyword.

    n - the number of values in the dataset. Should be greater than the total number of record ids in W.

    K - the tuple of secret keys related to building the index.
        Kpsi is used to generate addresses, key for PRP.
        Kpi is used for address of lookup table, key for PRP.
        Kphi is used to encrypt values, key for PRF.

    Klen - length of the keys to generate when encrypting the index.

    secretKey - a pairings secret key to encrypt keywords in final step.

    """
    ctr = 1 # Set global counter

    m = n * n * 2 + 113
    A = [None] * m # Array A creation

    (Kpsi, Kpi, Kphi) = K # retrieve keys
    nodes = [] # keeping track of each node (address in A and key)
    
    PsiCipher = AESCTR(Kpsi) # cipher for the PRP we use for ordering the array elements

    # Traverse each keyword in dataset
    for keyword, ids in W.items():
        kHead = os.urandom(Klen // 8) # generate random key ki,0 for first node

        # generate address in A for first node using key Kpsi
        while(True):
            psiCtr = PsiCipher.encryptor().encrypt(ctr.to_bytes(16, "big"))
            addrHead = int.from_bytes(psiCtr, 'big') % m
            if(A[addrHead] is None):
                break
            ctr = ctr + 1
        # #print("W_I:", keyword)

        # Traverse ids (vals) of keywords
        j=0
        nodes.append((addrHead.to_bytes(10, 'big'), kHead))
        for id in ids:
            # ##print('encrypt id:',id)
            kNext = os.urandom(Klen // 8) # generate key ki,j to encrypt/decrypt next node

            # if not last node in list, generate address of next node using key Kpsi
            if(j != len(W[keyword]) - 1):
                while(True):

                    # ##print('gen address for next node')
                    psiCtr = PsiCipher.encryptor().encrypt((ctr + 1).to_bytes(16, "big"))
                    addrNext = int.from_bytes(psiCtr, 'big') % m
                    if(A[addrNext] is None):
                        break
                    ctr = ctr + 1
            else:
                addrNext = None # last node

            # create node with record id, key of next node, and address in A of next node
            node = Node(id, kNext, addrNext)

            # Encrypt current node (N'ij) using prev key
            print('N(recID, kNext, addrNext):',node, " addr:", addrHead)
            ct = AESSIVEncryptNonce(kHead, str(node)) #use AESSIV for undeterministic symmetric encryption

            if(A[addrHead] is not None): # debugging, ##print if we have a collision
                ##print('Debug: Collision found')
                raise Exception("Collision Detected")

            # Store node in A (pseudorandom order)
            A[addrHead] = ct

            # store current node info (address in A, key) for lookuptable
            kHead = kNext # next node key
            addrHead = addrNext # next node address in A

            ctr = ctr+1 # increment counter
            j=j+1
        # #print()

    # TODO: Fill in remaining entries of A with random values

    # Look up table T creation for heads of each linked list
    T = {} # unsecure lookup table ! should use a secure table like cuckoo table
    nodeIndex = 0

    for keyword, ids in W.items():

        Ki = phiFunction(Kphi, keyword) #get key Ki to xor everything
        pos = pairing(g1.hash(bytes(keyword, 'utf-8')), g2 * secretKey)

        (addr, k) = nodes[nodeIndex] #retrieve addr in A and k of node
        # value = get_xor(addr + k, Ki) # combine addr+k, xor with val
        addr = bytes(addr ^ Ki for addr, Ki in zip(addr, cycle(Ki))) #addr xor Ki
        k = bytes(k ^ Ki for k, Ki in zip(k, cycle(Ki))) #k xor Ki

        T[str(pos)] = [(addr, k)] # create new value list for keyword
        nodeIndex = nodeIndex + 1

    I = (A, T)
    print("=====Index Created=====\nArray A length:", len(A), "\nLookup Table T length:", len(T.keys()))
    if(debugDetailed):
        #print(I)
        pass
        
    return I

