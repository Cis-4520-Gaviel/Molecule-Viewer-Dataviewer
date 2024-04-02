from Users import Writer, Reader
from pymcl import pairing, g1,g2

def testUserNoDatabase():
    writer = Writer(None, None)
    reader = Reader(None, None)
    indexHashed = writer.encryptKeyword("Name='Gaviel'")

    auth = writer.delegate(reader.getPublicKey())

    trapdoors = reader.trapdoor("SELECT * FROM PATIENT WHERE Name='Gaviel';")
    pos, hashedValue = list(trapdoors)[0]

    transformation = pairing(hashedValue, auth)
    print(indexHashed,"\n\n", transformation)
    print("matched: ", indexHashed == transformation)

if __name__ == '__main__':
    # main()
    testUserNoDatabase()