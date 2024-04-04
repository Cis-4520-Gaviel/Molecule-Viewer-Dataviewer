from users.Users import Writer, Reader
from pymcl import pairing, g1,g2
from database.QueryMultiplexer import QueryMutliplexer
from database.DataHost import DataHost
import random
import string
def printResults(results, query, readerId):
    print(f'\nSearch results when {readerId} searches {query}: {results}')

def testScheme():
    # init
    print(g1)
    print(g1)

    qm = QueryMutliplexer(b'123')
    dh = DataHost()
    writer = Writer(qm, dh, "Alice")
    reader = Reader(qm, dh, "Bob")
    reader2 = Reader(qm, dh, "Cathy")

    #table creation
    writer.updateDatabase(['Fire', 1, 1])
    writer.updateDatabase(['Water', 2, 1])
    writer.updateDatabase(['Earth', 1, 3])
    for i in range(100):
        writer.updateDatabase([''.join(random.choices(string.ascii_uppercase + string.digits, k=5)), random.randint(0,1000), random.randint(0,30)])
    writer.encrypt()
    # auth delegation

    dh.readerKeygen(reader.id, reader.getPublicKey())

    writer.delegate(reader.getPublicKey(), reader.id)
    #search query
    trapdoors = reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';", writer._keySet)
    tPrime = qm.transform(trapdoors, reader.id)
    # print(tPrime)
    printResults(dh.search(tPrime), "SELECT * FROM Molecules WHERE BOND_NO='1';", reader.id)

    t2 = reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1' AND NAME='Earth';", writer._keySet)
    tp2 = qm.transform(t2, reader.id)
    printResults(dh.search(tp2), "SELECT * FROM Molecules WHERE BOND_NO='1' AND NAME='Earth';", reader.id)

    badTrapdoor = reader2.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';", writer._keySet)
    badTrapdoors = qm.transform(badTrapdoor, reader2.id)

    printResults(dh.search(badTrapdoors), "SELECT * FROM Molecules WHERE BOND_NO='1';", reader2.id)

    print("\nQM Data\n")
    qm.printData()

if __name__ == '__main__':
    # main()
    testScheme()