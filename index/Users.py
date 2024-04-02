import os
from pymcl import Fr, g1, g2
from abc import ABC, abstractmethod
class User(ABC):
    @abstractmethod
    def _setup(self):
        pass

class Writer(User):
    def _setup(self):
        secretKey = Fr.random()
        return secretKey

    def __init__(self):
        self._secretKey = self._setup()

    #database

class Reader(User):
    def _setup(self):
        privateKey = Fr.random()
        publicKey = g2 * ~privateKey
        kR = os.urandom(8)
        return publicKey, privateKey, kR

    def __init__(self):
        publicKey, privateKey, kR = self._setup()
        self._publicKey = publicKey
        self._privateKey = privateKey
        self._kR = kR

    def getPublicKey(self):
        return self._publicKey