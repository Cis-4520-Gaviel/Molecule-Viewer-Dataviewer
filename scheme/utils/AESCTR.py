from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher, CipherContext
from NonceCipherContext import NonceEncryptContext, NonceDecryptContext
import os
# AES function for CTR mode
class AESCTR:
    """ This class automatically initializes a Cipher object for AES-CTR. 

        Methods:

        .encryptor() creates a cipherContext for encryption with the following key/nonce
            optional argument: nonce - provide a nonce instead of generating one
            
        .decryptor() create a cipherContext for decryption.
    """
    def __init__(self, key):
        # recommended thing
        self.key = key

    def encryptor(self, nonce = None) -> NonceEncryptContext:
        if(nonce is None):
            nonce = os.urandom(16)
            
        return NonceEncryptContext(Cipher(algorithms.AES(self.key), modes.CTR(nonce)).encryptor(), nonce) 
    
    def decryptor(self)  -> NonceDecryptContext:
        return NonceDecryptContext(self.key)