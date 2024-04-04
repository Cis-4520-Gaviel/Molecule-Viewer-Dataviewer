import os
from pymcl import Fr, g1, g2, pairing
from abc import ABC, abstractmethod
from Trapdoor import generateTrapdoor, generateTrapdoorBLS12381

class User(ABC):
    @abstractmethod
    def _setup(self):
        pass

    def __init__(self, queryMultiplexer, dataHost):
        self.QM = queryMultiplexer
        self.DH = dataHost

class Writer(User):
    """
    Writer user that interacts with the Gaviel scheme. Contains a single symmetric key
    Has the ability to delegate authorizations to readers, and encrypt a database
    """
    def _setup(self):
        secretKey = Fr.random()
        return secretKey

    def __init__(self, queryMultiplexer, dataHost):
        self._secretKey = self._setup()
        super().__init__(queryMultiplexer, dataHost)

    def delegate(self, readerPublicKey: Fr):
        """
        Authorize a reader via their public key
        """
        auth = readerPublicKey * self._secretKey
        #send to QM
        return auth

    def encrypt(self, index):
        yield Exception("not implemented yet")

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

    def __init__(self, queryMultiplexer, dataHost):
        publicKey, privateKey, kR = self._setup()
        self._publicKey = publicKey
        self._privateKey = privateKey
        self._kR = kR
        super().__init__(queryMultiplexer, dataHost)

    def getPublicKey(self) -> Fr:
        return self._publicKey
    
    def trapdoor(self, sqlStatement):
        test = generateTrapdoorBLS12381(sqlStatement, self._privateKey) # nuh uh
        return test
        # yield Exception("need to implement this")