import os
from KeyGen import KeyGen
from pymcl import Fr
class KeySet:
    def __init__(self, keylen = 256):
        self._psi, self._pi, self._phi = KeyGen(keylen)

    
    def getKeys(self):
        return (self._psi, self._pi, self._phi)