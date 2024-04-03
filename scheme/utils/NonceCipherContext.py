from cryptography.hazmat.primitives import ciphers, padding
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from cryptography.exceptions import AlreadyFinalized

# wrapper CipherContext to handle the addition of the nonce before the ciphertext when encrypting
class NonceEncryptContext:
    """ wrapper CipherContext to handle the addition of the nonce before the ciphertext when encrypting
    """
    def __init__(self, cipherContext: ciphers.CipherContext, nonce, CGM = False, requiresPadding = False):
        self.cipherContext = cipherContext
        self.nonce = nonce
        self.requiresPadding = requiresPadding
        self.hasCalled = False

    # only call update once, the context will be finalized during this call
    def encrypt(self, data):
        data = bytes(str(data), 'utf-8')
        # prevent multiple calls
        if(self.hasCalled):
            raise AlreadyFinalized()
        self.hasCalled = True

        if(self.requiresPadding):
            padder = padding.PKCS7.padder()
            paddedData = padder.update(data)
            paddedData += padder.finalize()
            data = paddedData

        self.ciphertext = self.nonce + self.cipherContext.update(data) + self.cipherContext.finalize()
        return self.ciphertext

# wrapper CipherContext to handle reading of the prefix nonce during decryption. 
# also handles CGM tag
class NonceDecryptContext:
    def __init__(self, key, CGM = False, hasPadding = False):
        self.hasPadding = hasPadding
        self.CGM = CGM
        self.key = key
        self.hasCalled = False

    # only call update once, the context will be finalized during this call
    def update(self, data):
        # prevent multiple calls
        if(self.hasCalled):
            raise AlreadyFinalized()
        self.hasCalled = True

        nonce = data[:12]
        ciphertext = data[12:]

        if(self.hasPadding):
            unpadder = padding.PKCS7.unpadder()
            ciphertext = unpadder.update(data[12:])

        self.cipherContext = Cipher(algorithms.AES(self.key), modes.CTR(nonce)).decryptor()
        
        self.plaintext = self.cipherContext.update(ciphertext)
        if(self.CGM):
            self.plaintext += self.cipherContext.finalize_with_tag()
        else:
            self.plaintext += self.cipherContext.finalize()
            
        return self.plaintext
class DecryptContext:
    def __init__(self, key, nonce, CGM = False, hasPadding = False):
        self.hasPadding = hasPadding
        self.CGM = CGM
        self.key = key
        self.hasCalled = False
        self.cipherContext = Cipher(algorithms.AES(self.key), modes.CTR(nonce)).decryptor()


    # only call update once, the context will be finalized during this call
    def update(self, data):
        # prevent multiple calls
        if(self.hasCalled):
            raise AlreadyFinalized()
        self.hasCalled = True

        ciphertext = data

        if(self.hasPadding):
            unpadder = padding.PKCS7.unpadder()
            ciphertext = unpadder.update(data[12:])

        
        self.plaintext = self.cipherContext.update(ciphertext)
        if(self.CGM):
            self.plaintext += self.cipherContext.finalize_with_tag()
        else:
            self.plaintext += self.cipherContext.finalize()
            
        return self.plaintext
