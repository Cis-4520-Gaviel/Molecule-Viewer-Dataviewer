import pymcl

def TestAuthorizationSystem():
    frTest = pymcl.Fr('4956860243094490671591998352430815023460385533631324063655048520527491662930')
    x1 = frTest.random()
    g1 = pymcl.g1
    g2 = pymcl.g2

    keyword = g1.hash(bytes("test", 'utf-8'))
    searchQuery = g1.hash(bytes("test", 'utf-8'))

    writerSecretKey = pymcl.Fr.random()
    privateKey = pymcl.Fr.random()
    public = g2 * ~privateKey

    authorization = public * writerSecretKey
    indexHash = pymcl.pairing(keyword, g2 * writerSecretKey)

    transformation = pymcl.pairing(searchQuery * privateKey, authorization)
    print(indexHash,"\n\n", transformation)
    print("Keys Match: ",indexHash == transformation)

if __name__ == '__main__':
    TestAuthorizationSystem()