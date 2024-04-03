from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes, CipherContext;
from cryptography.hazmat.primitives import padding;
import os
import Node
from AESCTR import AESCTR
import AESGCM
from NonceCipherContext import NonceDecryptContext, NonceEncryptContext

keyLength = 256
kStuff = 1
keyPsi = os.urandom(256//8)
testNonce = 'c'
def BuildDictionary(D):
    return {"test":[]}

def BuildIndex():
    PsiCipher = AESCTR(keyPsi)
    test = set()
    print(keyPsi)
    ctr = 1
    for x in range(1000):
        psuedoRandomPerm = PsiCipher.encryptor(ctr.to_bytes(16, "big"))
        
        psiCtr = psuedoRandomPerm.encrypt(testNonce)
        indexNum = int.from_bytes(psiCtr[16:], "big")
        print(psiCtr[16:].hex(), indexNum)

        # print("Address for ", ctr , ":" + str(int.from_bytes(psiCtr[16:], "big")))

        # if(indexNum in test):
        #     print("Address for ", ctr , ":" + str(int.from_bytes(psiCtr[16:], "big")))

        test.add(indexNum)
        ctr += 1
    

            

if __name__ == "__main__":
    BuildIndex()