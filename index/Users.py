import os
from pymcl import Fr, g1, g2
from abc import ABC, abstractmethod
from Trapdoor import generateTrapdoor

class User(ABC):
    @abstractmethod
    def _setup(self):
        pass

    def __init__(self, queryMultiplexer, dataHost):
        self.QM = queryMultiplexer
        self.DH = dataHost

class Writer(User):
    def _setup(self):
        secretKey = Fr.random()
        return secretKey

    def __init__(self, queryMultiplexer, dataHost):
        self._secretKey = self._setup()
        super(queryMultiplexer, dataHost)

    def delegate(self, readerPublicKey: Fr):
        auth = readerPublicKey * self._secretKey
        #send to QM

    def encrypt(self, index):
        yield Exception("not implemented yet")
    #database

class Reader(User):
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
        super(queryMultiplexer, dataHost)

    def getPublicKey(self):
        return self._publicKey
    
    def trapdoor(self, sqlStatement):
        yield Exception("need to implement this")
        generateTrapdoor(sqlStatement, 10) # nuh uh