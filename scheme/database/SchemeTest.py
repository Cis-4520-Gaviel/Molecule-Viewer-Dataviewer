from users.Users import Writer, Reader
from pymcl import pairing, g1,g2
from database.QueryMultiplexer import QueryMutliplexer
from database.DataHost import DataHost

def testScheme():
    # init
    qm = QueryMutliplexer(b'123')
    dh = DataHost()
    writer = Writer(qm, dh, "Alice")
    reader = Reader(qm, dh, "Bob")

    #table creation
    writer.updateDatabase(['Fire', 1, 1])
    writer.updateDatabase(['Water', 2, 1])
    writer.updateDatabase(['Earth', 1, 3])
    writer.encrypt()
    # auth delegation

    dh.readerKeygen(reader.id, reader.getPublicKey())

    writer.delegate(reader.getPublicKey(), reader.id)
    #search query
    trapdoors = reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';", writer._keySet)
    tPrime = qm.transform(trapdoors, reader.id)
    # print(tPrime)
    print(dh.search([tPrime]))

    # transformation = pairing(hashedValue, auth)
    # # print(indexHashed,"\n\n", transformation)
    # print("matched: ", indexHashed == transformation)
    # print("\nQM Data\n")
    # qm.printData()

if __name__ == '__main__':
    # main()
    testScheme()