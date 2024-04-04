from re import search
import Database
from users.BuildIndex import BuildIndexNewHash
from users.CreateDictionary import CreateDictionary
from Search import Search
class DataHost:
    def __init__(self) -> None:
        self._readerKeys = {}
        self._encryptedIndexes = {}
        pass

    def process(self, trapdoors):
        pass

    def readerKeygen(self, readerId, readerKey):
        self._readerKeys[readerId] = readerKey
    
    def uploadIndex(self, index, tableName: str): # replace this with more secure
        self._encryptedIndexes[tableName] = index

    def encryptTable(self, database: Database, tableName, k, secretKey):
        keywordList, n = CreateDictionary(database, tableName)
        I = BuildIndexNewHash(keywordList, n, K=k, Klen=256, secretKey=secretKey)
        self._encryptedIndexes[tableName] = I

    def search(self, t, tableName='Molecules'):
        R = Search(self._encryptedIndexes[tableName], t[0])
        return R
    