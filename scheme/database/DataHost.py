from termcolor import colored
from database.Database import Database
from database.BuildIndex import BuildIndex
from database.CreateDictionary import CreateDictionary
from database.Search import Search
from database.EncryptedDatabase import EncryptedDatabase
from cryptography.hazmat.primitives.ciphers import aead;
from utils.CryptoUtils import AESSIVDecryptNonce, AESSIVEncryptNonce
from utils.Records import convertTupleToString
class DataHost:
    def __init__(self, database : EncryptedDatabase = None) -> None:
        self._masterKey = aead.AESSIV.generate_key(256)
        self._readerKeys = {}
        self._encryptedIndexes = {}
        self._database = database
        self._encryptedTableAttributes = {}
        pass

    def addReader(self, readerId, readerKey):
        print(colored('DH', 'green'),'\t add reader [',colored(readerId, 'cyan'),']')
        self._readerKeys[readerId] = readerKey
        print(colored('DH', 'green'),'\t done add reader')
    
    def uploadIndex(self, index, tableName: str): # replace this with more secure
        """
        Allows an encrypted index to be set for a given encrypted table name
        """
        print(colored('DH', 'green'),'\t upload index')
        self._encryptedIndexes[tableName] = index
        print(colored('DH', 'green'),'\t done upload index')

    def encryptTable(self, database: Database, tableName, k, secretKey, realTableName):
        """
        given a database instance, generates an index for it using the given keys. Will store
        the database within this DataHost instance.
        """
        print(colored('DH', 'green'),'\t generate index for table')
        keywordList, n = CreateDictionary(database, realTableName)
        I = BuildIndex(keywordList, n, K=k, Klen=256, secretKey=secretKey)
        self._encryptedIndexes[tableName] = I
        print(colored('DH', 'green'),'\t done generate index')

    def Register(self, tableName: str, attributes: list):
        """
        Send the value of the normal string
        Attributes will be in the form from the sql commands
        """
        print(colored('DH', 'green'),'\t register new table')
        # encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()

        if(self._encryptedTableAttributes.get(tableName) is not None):
            return
        encryptedAttributes = []
        
        for attribute in attributes:
            c = AESSIVEncryptNonce(self._masterKey, attribute).hex()
            encryptedAttributes.append(c)

        self._encryptedTableAttributes[tableName] = encryptedAttributes

        self._database.createTable(tableName, encryptedAttributes)
        print(colored('DH', 'green'),'\t done register new table [',colored(tableName, 'yellow'),'] with attributes',encryptedAttributes)

    def UploadValues(self, tableName, values):
        """
        Allows adding/uploading new records to a given table. The table name must
        already be incrypted.
        """
        print(colored('DH', 'green'),'\t add new values to table')
        # encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()

        if(self._encryptedTableAttributes[tableName] is None):
            return
        
        recordId = self._database.getTableRecordLength(tableName) + 1
        encryptedValues = [recordId]
        for value in values:
            encValue = AESSIVEncryptNonce(self._masterKey,str(value),).hex()
            encryptedValues.append(encValue)

        self._database.insertIntoTable(tableName, self._encryptedTableAttributes[tableName], encryptedValues)
        print(colored('DH', 'green'),'\t done add new values [',encryptedValues,']')


    def search(self, t, readerId):
        """
        The search method. Recieves an array of trapdoor lists, one per writer authorized.
        """
        print(colored('DH', 'green'),'\t start search')
        # encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()
        r = self._readerKeys[readerId]
        tableIds = set(())
        if(len(t) == 0):
            print(colored('DH', 'green'),'\t search fail!')
            return tableIds, []
        allRecords = []

        #each iteration all belongs to the same table name, which belongs
        # to a one writer
        for tPrime in t:
            ids = set(())
            # The encrypted table name will be the same between all trapdoors here
            (temp, temp1, tableName) = tPrime[0] #get the table name here

            #performing the keyword serach for all trapdoors within tprime
            for trapdoor in tPrime:
                (pos, k, tName) = trapdoor
                print(colored('DH', 'green'),'\t get pos and sql table name from trapdoor')
                print(colored('DH', 'green'),'\t searching for pos [',pos,'] in table [',tName.serialize().hex(),']')
                print()
                results = Search(self._encryptedIndexes[tName.serialize().hex()], (pos, k))
                ids.update(results)
                print()
            records = []

            # processing the results if there are any found.
            if(len(ids) > 0):
                records = self._database.retrieveRecords(tableName.serialize().hex(), list(ids))
                newVals = []
                for record in records:
                    relevantRecords = record[1:]
                    print(colored('DH', 'green'),'\t decrypt',record, " - encrypt using " , colored(readerId, 'cyan'), "'s secret key")
                    unencryptedRecord = []

                    #encrypt the records wtih k[r] before returning
                    for val in relevantRecords:
                        unencryptedRecord.append(AESSIVDecryptNonce(self._masterKey, bytes.fromhex(val)).decode('utf-8'))
                    newVals.append(AESSIVEncryptNonce(r,convertTupleToString(unencryptedRecord)))
                allRecords.extend(newVals)
                tableIds.update(ids)
        
        print(colored('DH', 'green'),'\t done search [',ids,allRecords,']')
        return tableIds, allRecords
    