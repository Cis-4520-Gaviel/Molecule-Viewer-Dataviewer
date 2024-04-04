import sqlparse
from utils.CryptoUtils import AESSIVEncryptNonce, phiFunction, get_xor
from pymcl import g1, pairing
import os
from sql.Parser import getSelectKeywords

def generateTrapdoor(sql, K):
    """
    generates an array of trapdoors from a select sql statement containing one or more queries
    """
    (Kpsi, Kpi, Kphi) = K # retrieve keys
    print('input SQL:', sql)
    keywords = ExtractKeywords(sql)
    # print('extract keywords:', keywords)
    # AESSIVEncryptNonce(K, keywords[0])
    trapdoors = []
    for keyword in keywords:
        print('extract keyword:', keyword)
        pos = keyword
        Kw = phiFunction(Kphi, keyword) #get key Kw (same as Ki from lookuptable creation)
        # print('get Kw', Kw, 'of type', type(Kw))
        trapdoors.append((pos, Kw))
    return trapdoors
    
def generateTrapdoorBLS12381(sql, privKey):
    """
    generates an array of trapdoors from a select sql statement containing one or more queries
    """
    # (Kpsi, Kpi, Kphi) = K # realistically we would be generating our own curve, but for this case we use the predefined ones
    print('input SQL:', sql)
    keywords = getSelectKeywords(sql)
    # print('extract keywords:', keywords)
    # AESSIVEncryptNonce(K, keywords[0])
    trapdoors = []
    for keyword in keywords:
        print('extract keyword:', keyword)
        pos = keyword
        Kw = g1.hash(bytes(keyword, 'utf-8')) #get key Kw (same as Ki from lookuptable creation)
        encVal = Kw * privKey
        # print('get Kw', Kw, 'of type', type(Kw))
        trapdoors.append((pos, encVal))
    return trapdoors
    


if __name__ == "__main__":
        key = os.urandom(16)
        t = generateTrapdoor("""SELECT * FROM PATIENT WHERE Name='Mary' AND Surname='Grant';""" , key)
        t2 = generateTrapdoor("""SELECT * FROM PATIENT WHERE Name='Mary';""" , key)
        print('trapdoor', t)
        print('second trapdoor', t2)
    
