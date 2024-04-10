from utils.CryptoUtils import phiFunction
from pymcl import g1
import os
from sql.Parser import getSelectKeywords

def generateTrapdoor(sql, privKey): #using new hash
    """
    generates an array of trapdoors from a select sql statement containing one or more queries
    """
    Kphi = b''
    # (Kpsi, Kpi, Kphi) = K # retrieve keys
    print('input SQL:', sql)

    keywords = getSelectKeywords(sql)
    tableName = 'Molecules'
    encTableName = g1.hash(bytes(tableName, 'utf-8')) * privKey

    trapdoors = []
    for keyword in keywords:
        print('extract keyword:', keyword)
        posHash = g1.hash(bytes(keyword, 'utf-8'))
        pos = posHash * privKey
        Kw = phiFunction(Kphi, keyword) #get key Kw (same as Ki from lookuptable creation)
        # #print('get Kw', Kw, 'of type', type(Kw))
        trapdoors.append((pos, Kw, encTableName))
    print('generate trapdoors:',trapdoors)
    return trapdoors


if __name__ == "__main__":
        key = os.urandom(16)
        t = generateTrapdoor("""SELECT * FROM PATIENT WHERE Name='Mary' AND Surname='Grant';""" , key)
        t2 = generateTrapdoor("""SELECT * FROM PATIENT WHERE Name='Mary';""" , key)
        #print('trapdoor', t)
        #print('second trapdoor', t2)
    
