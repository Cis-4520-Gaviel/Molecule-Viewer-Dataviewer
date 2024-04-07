from re import search
import Database
from users.BuildIndex import BuildIndexNewHash
from users.CreateDictionary import CreateDictionary
from Search import Search
from EncryptedDatabase import EncryptedDatabase
from cryptography.hazmat.primitives.ciphers import aead;
class DataHost:
    def __init__(self, database : EncryptedDatabase = None) -> None:
        self._masterKey = aead.AESSIV.generate_key(256)
        self._readerKeys = {}
        self._encryptedIndexes = {}
        self._database = database
        self._encryptedTableAttributes = {}
        pass

    def addReader(self, readerId, readerKey):
        print('DH: add reader [',readerId,']')
        self._readerKeys[readerId] = readerKey
        print('DH: done add reader')
    
    def uploadIndex(self, index, tableName: str): # replace this with more secure
        print('DH: upload index')
        self._encryptedIndexes[tableName] = index
        print('DH: done upload index')

    def encryptTable(self, database: Database, tableName, k, secretKey, realTableName):
        print('DH: generate index for table')
        keywordList, n = CreateDictionary(database, realTableName)
        I = BuildIndexNewHash(keywordList, n, K=k, Klen=256, secretKey=secretKey)
        self._encryptedIndexes[tableName] = I
        print('DH: done generate index')

    def registerNewTable(self, tableName: str, attributes: list):
        """
        Send the value of the normal string
        Attributes will be in the form from the sql commands
        """
        print('DH: register new table')
        cipher = aead.AESSIV(self._masterKey)
        # encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()

        if(self._encryptedTableAttributes.get(tableName) is not None):
            return
        encryptedAttributes = []
        
        for attribute in attributes:
            c = cipher.encrypt(bytes(attribute, 'utf-8'), []).hex()
            encryptedAttributes.append(c)

        self._encryptedTableAttributes[tableName] = encryptedAttributes

        self._database.createTable(tableName, encryptedAttributes)
        print('DH: done register new table [',tableName,'] with attributes',encryptedAttributes)

    def addNewValuesToTable(self, tableName, values):
        print('DH: add new values to table')
        cipher = aead.AESSIV(self._masterKey)
        # encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()

        if(self._encryptedTableAttributes[tableName] is None):
            return
        
        recordId = self._database.getTableRecordLength(tableName) + 1
        encryptedValues = [recordId]
        for value in values:
            encValue = cipher.encrypt(bytes(str(value), 'utf-8'), []).hex()
            encryptedValues.append(encValue)

        self._database.insertIntoTable(tableName, self._encryptedTableAttributes[tableName], encryptedValues)
        print('DH: done add new values [',encryptedValues,']')


    def search(self, t):
        print('DH: start search')
        cipher = aead.AESSIV(self._masterKey)
        # encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()
        ids = set(())
        if(len(t) == 0):
            print('DH: search fail!')
            return ids, []
        (temp, temp1, tableName) = t[0]
        for trapdoor in t:
            (pos, k, tName) = trapdoor
            print('DH: get pos and sql table name from trapdoor')
            print('DH: searching for pos [',pos,'] in table [',tName.serialize().hex(),']')
            print()
            results = Search(self._encryptedIndexes[tName.serialize().hex()], (pos, k))
            ids.update(results)
            print()
        records = []
        if(len(ids) > 0):
            records = self._database.retrieveRecords(tableName.serialize().hex(), list(ids))
            newVals = []
            for record in records:
                relevantRecords = record[1:]
                print('DH: decrypt',record)
                unencryptedRecord = []
                for val in relevantRecords:
                    unencryptedRecord.append(cipher.decrypt(bytes.fromhex(val),[]).decode('utf-8'))
                newVals.append(unencryptedRecord)
            records = newVals
        
        print('DH: done search [',ids,records,']')
        return ids, records
    