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

    def readerKeygen(self, readerId, readerKey):
        self._readerKeys[readerId] = readerKey
    
    def uploadIndex(self, index, tableName: str): # replace this with more secure
        self._encryptedIndexes[tableName] = index

    def encryptTable(self, database: Database, tableName, k, secretKey):
        keywordList, n = CreateDictionary(database, tableName)
        I = BuildIndexNewHash(keywordList, n, K=k, Klen=256, secretKey=secretKey)
        self._encryptedIndexes[tableName] = I

    def registerNewTable(self, tableName: str, attributes: list):
        """
        Send the value of the normal string
        Attributes will be in the form from the sql commands
        """
        cipher = aead.AESSIV(self._masterKey)
        encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()

        if(self._encryptedTableAttributes.get(encTableName) is not None):
            return
        encryptedAttributes = []
        
        for attribute in attributes:
            c = cipher.encrypt(bytes(attribute, 'utf-8'), []).hex()
            encryptedAttributes.append(c)

        self._encryptedTableAttributes[encTableName] = encryptedAttributes

        self._database.createTable(encTableName, encryptedAttributes)

    def addNewValuesToTable(self, tableName, values):
        cipher = aead.AESSIV(self._masterKey)
        encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()

        if(self._encryptedTableAttributes[encTableName] is None):
            return
        
        recordId = self._database.getTableRecordLength(encTableName) + 1
        encryptedValues = [recordId]
        for value in values:
            encValue = cipher.encrypt(bytes(str(value), 'utf-8'), []).hex()
            encryptedValues.append(encValue)

        self._database.insertIntoTable(encTableName, self._encryptedTableAttributes[encTableName], encryptedValues)


    def search(self, t, tableName='Molecules'):
        cipher = aead.AESSIV(self._masterKey)
        encTableName = cipher.encrypt(bytes(tableName, 'utf-8'),[]).hex()

        results = set(())
        
        for trapdoor in t:
            results.update(Search(self._encryptedIndexes[tableName], trapdoor))
        values = []
        if(len(results) > 0):
            values = self._database.retrieveRecords(encTableName, list(results))
        
        return results, values
    