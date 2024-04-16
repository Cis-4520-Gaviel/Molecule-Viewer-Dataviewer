from utils.CryptoUtils import phiFunction
from pymcl import g1
import os
from sql.Parser import getSelectKeywords

def generateTrapdoor(sql, privKey, tableName = 'Molecules'): #using new hash
    """
    generates an array of trapdoors from a select sql statement containing one or more queries
    tableName defaults to "Molecules" for old code, which could not be refactored in time.
    """
    Kphi = b''
    # (Kpsi, Kpi, Kphi) = K # retrieve keys
    print('input SQL:', sql)
    try:
        keywords = getSelectKeywords(sql) # TODO retrieve tablename from getSelectKeywords and use here
    except:
         print("Invalid SQL Statement")
         raise Exception()
    
    encTableName = g1.hash(bytes(tableName, 'utf-8')) * privKey

    trapdoors = []
    for keyword in keywords: #created a new trapdoor for each keyword condition found
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
    
