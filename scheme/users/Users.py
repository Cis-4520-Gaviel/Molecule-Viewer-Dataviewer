import os
from pymcl import Fr, g1, g2, pairing
from abc import ABC, abstractmethod
from users.Trapdoor import generateTrapdoor, generateTrapdoorBLS12381
from database.QueryMultiplexer import QueryMutliplexer
from database.DataHost import DataHost
from KeyGen import KeyGen
from database.Database import Database
from sql.Parser import parseInsertStatement
class User(ABC):
    @abstractmethod
    def _setup(self):
        pass

    def __init__(self, queryMultiplexer : QueryMutliplexer, dataHost: DataHost, id: str):
        self.QM = queryMultiplexer
        self.DH = dataHost
        self.id = id

class Writer(User):
    """
    Writer user that interacts with the Gaviel scheme. Contains a single symmetric key
    Has the ability to delegate authorizations to readers, and encrypt a database
    """
    def _setup(self):
        secretKey = Fr.random()
        self._keySet = KeyGen(256)
        return secretKey

    def __init__(self, queryMultiplexer, dataHost, id):
        self._secretKey = self._setup()
        self._database = Database(True)
        self._database.create_tables()
        super().__init__(queryMultiplexer, dataHost, id)
        self.QM.addWriter(self._secretKey, self.id)
        self.DH.registerNewTable('Molecules', ['NAME', 'ATOM_NO', 'BOND_NO'])
        

    def updateDatabase(self, values, rebuildIndex = False):
        self._database.add_molecule(*values)
        self.DH.addNewValuesToTable('Molecules', values)
        if(rebuildIndex == True):
            self.encrypt('Molecules')

    def delegate(self, readerPublicKey: Fr, readerId: str):
        """
        Authorize a reader via their public key
        """
        auth = readerPublicKey * self._secretKey
        self.QM.delegate(auth, self.id, readerId)
        return auth

    def encrypt(self, tableName = 'Molecules'):
        self.DH.encryptTable(self._database, tableName, self._keySet, secretKey=self._secretKey)

    def encryptKeyword(self, keyword):
        return pairing(g1.hash(bytes(keyword, 'utf-8')), g2 * self._secretKey)
    #database

class Reader(User):
    """
    A reader user in the Gaviel scheme. Has a pair of private and public keys, as well as
    a symmetric key for transforming their search queries (trapdoors)
    """
    def _setup(self):
        privateKey = Fr.random()
        publicKey = g2 * ~privateKey
        kR = os.urandom(8)
        return publicKey, privateKey, kR

    def __init__(self, queryMultiplexer, dataHost, id):
        publicKey, privateKey, kR = self._setup()
        self._publicKey = publicKey
        self._privateKey = privateKey
        self._kR = kR
        super().__init__(queryMultiplexer, dataHost, id)
        self.QM.addReader(self._publicKey, self.id)

    def getPublicKey(self) -> Fr:
        return self._publicKey
    
    def trapdoor(self, sqlStatement):
        test = generateTrapdoorBLS12381(sqlStatement, self._privateKey) # nuh uh
        return test
        # yield Exception("need to implement this")
    def trapdoor(self, sqlStatement, DEBUGKEYSET):
        test = generateTrapdoor(sqlStatement, DEBUGKEYSET, self._privateKey) # nuh uh
        return test