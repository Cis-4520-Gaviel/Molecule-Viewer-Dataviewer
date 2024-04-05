import os
from utils.Node import Node
from utils.AESCTR import AESCTR
from cuckoopy import CuckooFilter
from utils.CryptoUtils import AESSIVDecryptNonce, AESSIVEncryptNonce, phiFunction
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
from users.CreateDictionary import GetKeyAtValue
from itertools import cycle
from pymcl import pairing, g1, g2

# Generate a search index I
def BuildIndex(W,n,K,Klen):
    """
    Kpsi is used to generate addresses, key for PRP
    Kpi is used for address of lookup table, key for PRP
    Kphi is used to encrypt values, key for PRF
    """

    ctr = 1 # Set global counter

    m = 100
    A = [None] * m # Array A creation

    (Kpsi, Kpi, Kphi) = K # retrieve keys
    nodes = [] # keeping track of each node (address in A and key)
    
    PsiCipher = AESCTR(Kpsi) # cipher for the PRP we use for ordering the array elements

    # Traverse each keyword
    for keyword, ids in W.items():

        # keyword = GetKeyAtValue(W, i) # get keyword
        print('at keyword:', keyword)

        kHead = os.urandom(Klen // 8) # generate random key ki,0 for first node

        # generate address in A for first node using key Kpsi
        psuedoRandomPerm = PsiCipher.encryptor((1).to_bytes(16, "big"))
        psiCtr = psuedoRandomPerm.encrypt(ctr.to_bytes(16, "big"))
        addrHead = int.from_bytes(psiCtr, 'big') % m

        # Traverse ids (vals) of keywords
        j=0
        for id in ids:
            
            # print('encrypt id:',id)
            kNext = os.urandom(Klen // 8) # generate key ki,j to encrypt/decrypt next node

            # if not last node in list, generate address of next node using key Kpsi
            if(j != len(W[keyword]) - 1):
                print('gen address for next node')
                psuedoRandomPerm = PsiCipher.encryptor((1).to_bytes(16, "big"))
                psiCtr = psuedoRandomPerm.encrypt((ctr + 1).to_bytes(16, "big"))
                addrNext = int.from_bytes(psiCtr, 'big') % m
            else:
                addrNext = None # last node

            # create node with record id, key of next node, and address in A of next node
            node = Node(id, kNext, addrNext)

            # Encrypt current node (N'ij) using prev key
            aessiv = AESSIV(kHead) #encrypting each node with non deterministic encryptor
            print('encrypt node:',node)
            ct = aessiv.encrypt(bytes(str(node),'utf-8'), None) #use AESSIV for undeterministic symmetric encryption

            # if(A[nodeIndex] is not None): # debugging, print if we have a collision
            #     print('Debug: Collision found')

            # Store node in A (pseudorandom order)
            A[addrHead] = ct
            print('store encrypted node at address', addrHead)
            # print('A:', A)

            # store current node info (address in A, key) for lookuptable
            nodes.append((addrHead.to_bytes(1, 'big'), kHead))

            kHead = kNext # next node key
            addrHead = addrNext # next node address in A

            ctr = ctr+1 # increment counter
            j=j+1
            print()

    # TODO: Fill in remaining entries of A with rando values

    # Look up table T creation
    T = {} # unsecure lookup table ! should use a secure table like cuckoo table
    nodeIndex = 0
    # TODO: store info in T in pseudorandom order using key Kpi
    for keyword, ids in W.items():
        # print('encrypt keyword:', keyword)

        # Traverse ids (vals) of keywords
        j=0
        for id in ids:
            # print('encrypt id2:',id)
            Ki = phiFunction(Kphi, keyword) #get key Ki

            (addr, k) = nodes[nodeIndex] #retrieve addr in A and k of node
            # print('get addr:', addr, 'of type', type(addr))
            # print('real address:', int.from_bytes(addr,'big'))
            # print('get k:', k, 'of type', type(k))
            # print('get Ki', Ki, 'of type', type(Ki))

            # value = get_xor(addr + k, Ki) # combine addr+k, xor with val
            addr = bytes(addr ^ Ki for addr, Ki in zip(addr, cycle(Ki))) #addr xor Ki
            k = bytes(k ^ Ki for k, Ki in zip(k, cycle(Ki))) #k xor Ki

            if keyword in T:
                T[keyword].append((addr, k)) # add to value list of keyword
            else:
                T[keyword] = [(addr, k)] # create new value list for keyword
            
            nodeIndex = nodeIndex+1
    

    I = (A, T)

    return I

def BuildIndexNewHash(W,n,K,Klen, secretKey):
    """
    Kpsi is used to generate addresses, key for PRP
    Kpi is used for address of lookup table, key for PRP
    Kphi is used to encrypt values, key for PRF
    """
    ctr = 1 # Set global counter

    m = 1010 * n
    A = [None] * m # Array A creation

    (Kpsi, Kpi, Kphi) = K # retrieve keys
    nodes = [] # keeping track of each node (address in A and key)
    
    PsiCipher = AESCTR(Kpsi) # cipher for the PRP we use for ordering the array elements

    # Traverse each keyword
    for keyword, ids in W.items():
        kHead = os.urandom(Klen // 8) # generate random key ki,0 for first node

        # generate address in A for first node using key Kpsi
        psuedoRandomPerm = PsiCipher.encryptor((1).to_bytes(16, "big"))
        psiCtr = psuedoRandomPerm.encrypt(ctr.to_bytes(16, "big"))
        addrHead = int.from_bytes(psiCtr, 'big') % m
        print("W_I:", keyword)

        # Traverse ids (vals) of keywords
        j=0
        nodes.append((addrHead.to_bytes(10, 'big'), kHead))
        for id in ids:
            # print('encrypt id:',id)
            kNext = os.urandom(Klen // 8) # generate key ki,j to encrypt/decrypt next node

            # if not last node in list, generate address of next node using key Kpsi
            if(j != len(W[keyword]) - 1):
                # print('gen address for next node')
                psuedoRandomPerm = PsiCipher.encryptor((1).to_bytes(16, "big"))
                psiCtr = psuedoRandomPerm.encrypt((ctr + 1).to_bytes(16, "big"))
                addrNext = int.from_bytes(psiCtr, 'big') % m
            else:
                addrNext = None # last node

            # create node with record id, key of next node, and address in A of next node
            node = Node(id, kNext, addrNext)

            # Encrypt current node (N'ij) using prev key
            print('N(recID, kNext, addrNext):',node, " addr:", addrHead)
            ct = AESSIVEncryptNonce(kHead, str(node)) #use AESSIV for undeterministic symmetric encryption

            if(A[addrHead] is not None): # debugging, print if we have a collision
                print('Debug: Collision found')
                raise Exception("hi")

            # Store node in A (pseudorandom order)
            A[addrHead] = ct

            # store current node info (address in A, key) for lookuptable
            kHead = kNext # next node key
            addrHead = addrNext # next node address in A

            ctr = ctr+1 # increment counter
            j=j+1
        print()

    # TODO: Fill in remaining entries of A with rando values

    # Look up table T creation
    T = {} # unsecure lookup table ! should use a secure table like cuckoo table
    nodeIndex = 0

    # TODO: store info in T in pseudorandom order using key Kpi
    for keyword, ids in W.items():
        # print('encrypt keyword:', keyword)

        # print('encrypt id2:',id)
        Ki = phiFunction(Kphi, keyword) #get key Ki

        pos = pairing(g1.hash(bytes(keyword, 'utf-8')), g2 * secretKey)

        (addr, k) = nodes[nodeIndex] #retrieve addr in A and k of node
        # print('get addr:', addr, 'of type', type(addr))
        # print('real address:', int.from_bytes(addr,'big'))
        # print('get k:', k, 'of type', type(k))
        # print('get Ki', Ki, 'of type', type(Ki))

        # value = get_xor(addr + k, Ki) # combine addr+k, xor with val
        addr = bytes(addr ^ Ki for addr, Ki in zip(addr, cycle(Ki))) #addr xor Ki
        k = bytes(k ^ Ki for k, Ki in zip(k, cycle(Ki))) #k xor Ki

        T[str(pos)] = [(addr, k)] # create new value list for keyword
        nodeIndex = nodeIndex + 1

    I = (A, T)
    return I

def EncryptTable(T, K):
    attributes = ['stuff', 'stuff2'] # mock data

    for attribute in attributes:
        encryptedAttribute = AESSIVEncryptNonce(K, attribute)
    
    records = [('value1', 'value2'), ('value3', 'value4')] # mock data
    for i in range(len(records)):
        record = records[i]
        for value in record:
            encryptedValue = AESSIVEncryptNonce(K, value)

def DecryptTable(T, K):
    attributes = ['stuff', 'stuff2'] # mock data

    for attribute in attributes:
        decryptedAttribute = AESSIVDecryptNonce(K, attribute)
    
    records = [('value1', 'value2'), ('value3', 'value4')] # mock data
    for i in range(len(records)):
        record = records[i]
        for value in record:
            decryptedValue = AESSIVDecryptNonce(K, value)
    



# testKey = os.urandom(32)
# testVar = AESSIVEncryptNonce(testKey, 'among us')
# print(testVar.hex())
# result = AESSIVDecryptNonce(testKey, testVar)
# print(result)

