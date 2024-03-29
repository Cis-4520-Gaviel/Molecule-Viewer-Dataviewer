import os
from cryptography.hazmat.primitives.ciphers import aead

def KeyGen(Klen):
    
    Kpsi = os.urandom(Klen//8)
    Kpi = os.urandom(Klen//8)
    Kphi = aead.AESSIV.generate_key(Klen)

    return Kpsi, Kpi, Kphi

