import os
from cryptography.hazmat.primitives.ciphers import aead;
from cryptography.hazmat.primitives import hashes;

def AESSIVEncryptNonce(k, data, nonceLength = 12):
    typecastedData = bytes(data, 'utf-8')
    nonce = os.urandom(nonceLength)
    aessiv = aead.AESSIV(k)
    ciphertext = aessiv.encrypt(typecastedData, [nonce])
    return nonce + ciphertext

def AESSIVDecryptNonce(k, ciphertext, nonceLength = 12):
    nonce = ciphertext[:nonceLength]
    data = ciphertext[nonceLength:]
    aessiv = aead.AESSIV(k)
    return aessiv.decrypt(data, [nonce])

def AESOFBDigest(k, data):
    nonce = hashes.Hash(hashes.SHA256())

def phiFunction (k, keyword):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(bytes(keyword, "utf-8"))
    val = digest.finalize()
    return val

# https://www.geeksforgeeks.org/xor-two-binary-strings-of-unequal-lengths/
def get_xor(a, b):
    result = ""                 # Initialize an empty string to store the XOR result
    n = len(a)                  
    m = len(b)                 
    length = max(n, m)         
     
    for i in range(length):     # Iterate through each bit position
        x = int(a[n - i - 1]) if i < n else 0   # Get i-th bit of 'a' or 0 if it doesn't exist
        y = int(b[m - i - 1]) if i < m else 0   # Get i-th bit of 'b' or 0 if it doesn't exist
        z = x ^ y               # Calculate XOR of x and y
        result = str(z) + result               # Prepend the XOR result to the 'result' string
     
    return result
