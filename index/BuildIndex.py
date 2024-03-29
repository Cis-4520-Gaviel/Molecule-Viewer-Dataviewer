import os
from Node import Node
from AESCTR import AESCTR
from cuckoopy import CuckooFilter
from CryptoUtils import AESSIVDecryptNonce, AESSIVEncryptNonce, phiFunction, get_xor
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
from CreateDictionary import GetKeyAtValue
from itertools import cycle

mockVal = bytes('aa', 'utf-8')

GCMIV = os.urandom(12)

# Generate a search index I
def BuildIndex(W,n,K,Klen):

    ctr = 1 # Set global counter

    m = 100
    A = [None] * m # Array A creation

    (Kpsi, Kpi, Kphi) = K # retrieve keys
    nodes = [] # keeping track of each node (address in A and key)
    ids = [] # keeping track of traversed ids
    
    PsiCipher = AESCTR(Kpsi) # cipher for the PRP we use for ordering the array elements

    # Traverse each keyword
    for i in range(1, n+1):

        keyword = GetKeyAtValue(W, i) # get keyword
        print('at keyword:', keyword)

        #create linked list and the address of n1,j
        # addressGenerator = PsiCipher.encryptor((1).to_bytes(16, "big"))
        # head = addressGenerator.encrypt(ctr.to_bytes(16, "big"))
        # print('head:',head)

        kHead = os.urandom(Klen // 8) # generate random key ki,0 for first node

        # generate address in A for first node using key Kpsi
        psuedoRandomPerm = PsiCipher.encryptor((1).to_bytes(16, "big"))
        psiCtr = psuedoRandomPerm.encrypt(ctr.to_bytes(16, "big"))
        # print(int.from_bytes(curAddr, 'big') % 1000)
        addrHead = int.from_bytes(psiCtr, 'big') % m

        # Traverse ids (vals) of keywords
        for j in range(len(W[keyword])):

            id = W[keyword][j] # retrieve record id

            if id in ids: # check if id already traversed
                # print(W[keyword][j], 'already exists!\n')
                continue
            else:
                ids.append(id)
            
            # print('encrypt id:', W[keyword][j], 'from j index', j)
            kNext = os.urandom(Klen // 8) # generate key ki,j to encrypt/decrypt next node

            # if not last node in list, generate address of next node using key Kpsi
            if(j != len(W[keyword]) - 1):
                psuedoRandomPerm = PsiCipher.encryptor((1).to_bytes(16, "big"))
                psiCtr = psuedoRandomPerm.encrypt((ctr + 1).to_bytes(16, "big"))
                addrNext = int.from_bytes(psiCtr, 'big') % m
                # node.setNextAddress(psiCtr)
                print('new address gen!')
            else:
                addrNext = None # last node

            # create node with record id, key of next node, and address in A of next node
            node = Node(id, kNext, addrNext)

            # Encrypt current node (N'ij) using prev key
            aessiv = AESSIV(kHead) #encrypting each node with non deterministic encryptor
            # nonce = os.urandom(16)      #generating a 128-bit nonce
            print('encrypt node:',node,'of type',type(node))
            ct = aessiv.encrypt(bytes(str(node),'utf-8'), None) #use AESSIV for undeterministic symmetric encryption

            # if(A[nodeIndex] is not None): # debugging, print if we have a collision
            #     print('Debug: Collision found')

            # Store node in A (pseudorandom order)
            A[addrHead] = ct
            print('store encrypted node at address', addrHead, 'with val', ct)
            # print('A:', A)

            # store current node info (address in A, key) for lookuptable
            nodes.append((addrHead.to_bytes(1, 'big'), kHead))

            kHead = kNext # next node key
            addrHead = addrNext # next node address in A

            ctr = ctr+1 # increment counter
            print()

    # TODO: Fill in remaining entries of A with rando values

    # Look up table T creation
    T = {} # unsecure lookup table ! should use a secure table like cuckoo table
    # TODO: store info in T in pseudorandom order using key Kpi
    for i in range(1, n+1):
        keyword = GetKeyAtValue(W, i) #retrieve keyword
        Ki = phiFunction(Kphi, keyword) #get key Ki
        # print('encrypt keyword:', keyword)

        (addr, k) = nodes[i-1] #retrieve addr in A and k of node
        # print('get addr:', addr, 'of type', type(addr))
        # print('real address:', int.from_bytes(addr,'big'))
        # print('get k:', k, 'of type', type(k))
        # print('get Ki', Ki, 'of type', type(Ki))

        # value = get_xor(addr + k, Ki) # combine addr+k, xor with val
        addr = bytes(addr ^ Ki for addr, Ki in zip(addr, cycle(Ki))) #addr xor Ki
        k = bytes(k ^ Ki for k, Ki in zip(k, cycle(Ki))) #k xor Ki

        if keyword in T:
            T[keyword].append(addr, k) # add to value list of keyword
        else:
            T[keyword] = [(addr, k)] # create new value list for keyword
    
    
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

