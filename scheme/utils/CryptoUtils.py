import os
from cryptography.hazmat.primitives.ciphers import aead;
from cryptography.hazmat.primitives import hashes;
from itertools import cycle


def AESSIVEncryptNonce(k : bytes, data : str, nonceLength = 12) -> bytes:
    """
    Using AESSIV, encrypts given data, using a nonce of given length
    Default nonce length is 12.
    The nonce will automatically be appended to the beginning of the ciphertext
    """
    typecastedData = bytes(data, 'utf-8')
    nonce = os.urandom(nonceLength)
    aessiv = aead.AESSIV(k)
    ciphertext = aessiv.encrypt(typecastedData, [nonce])
    return nonce + ciphertext

def AESSIVDecryptNonce(k, ciphertext, nonceLength = 12) -> bytes:
    """
    Using AESSIV, decrypts a given ciphertext. The nonce is expected to be attached before
    the ciphertext, and has a length matching the given nonceLength
    """
    nonce = ciphertext[:nonceLength]
    data = ciphertext[nonceLength:]
    aessiv = aead.AESSIV(k)
    return aessiv.decrypt(data, [nonce])

def phiFunction (k, keyword) -> bytes:
    """
    Performs the phi function. In this case, we are using SHA-256
    """
    digest = hashes.Hash(hashes.SHA256())
    digest.update(bytes(keyword, "utf-8"))
    val = digest.finalize()
    return val

def xor(a, b) -> bytes:
    result = bytes(a ^ b for a, b in zip(a, cycle(b)))
    return result