from Users import Writer, Reader
from pymcl import pairing, g1,g2
from database.QueryMultiplexer import QueryMutliplexer
def testUserNoDatabase():
    qm = QueryMutliplexer(b'123')
    writer = Writer(qm, None, "Alice")
    reader = Reader(qm, None, "Bob")
    indexHashed = writer.encryptKeyword("Name='Gaviel'")

    auth = writer.delegate(reader.getPublicKey(), reader.id)

    trapdoors = reader.trapdoor("SELECT * FROM PATIENT WHERE Name='Gaviel';")
    pos, hashedValue = list(trapdoors)[0]

    transformation = pairing(hashedValue, auth)
    # print(indexHashed,"\n\n", transformation)
    print("matched: ", indexHashed == transformation)
    print("\nQM Data\n")
    qm.printData()

if __name__ == '__main__':
    # main()
    testUserNoDatabase()