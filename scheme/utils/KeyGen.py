import os
from cryptography.hazmat.primitives.ciphers.aead import AESSIV

def KeyGen(Klen):

    Kpsi = os.urandom(Klen//8)
    Kpi = os.urandom(Klen//8)
    Kphi = AESSIV.generate_key(Klen)

    return Kpsi, None, None

