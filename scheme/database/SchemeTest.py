from termcolor import colored
from users.Users import Writer, Reader
from pymcl import pairing, g1,g2
from database.QueryMultiplexer import QueryMutliplexer
from database.DataHost import DataHost
from EncryptedDatabase import EncryptedDatabase
import random
import string
import time
def printResults(results, query, readerId):
    ids, records = results
    print()
    print(f'Search results when [ {readerId} ] searches [ {query} ]:')
    print('ids:',ids)
    print('records:',records)
    print()

def testScheme():
    # init
    # print(g1)
    # print(g1)

    
    # init QM and DH
    qm = QueryMutliplexer(b'123')
    dh = DataHost(EncryptedDatabase(True))

    # init writer and readers
    print('Initializing users...')
    writer = Writer(qm, dh, "Alice")
    print()
    reader = Reader(qm, dh, "Bob")
    print()
    reader2 = Reader(qm, dh, "Cathy")
    print('Completed initializing users!\n\n')
    input()

    # table creation
    print('Adding records to db...')
    writer.updateDatabase(['Fire', 1, 1])
    writer.updateDatabase(['Water', 2, 1])
    writer.updateDatabase(['Earth', 1, 3])
    # for i in range(10):
    #     writer.updateDatabase([''.join(random.choices(string.ascii_uppercase + string.digits, k=5)), random.randint(0,1000), random.randint(0,30)])
    # writer.updateDatabase(['Joel', 69, 12], True)
    # writer.updateDatabase(['Myron', 100, 11], True)
    # writer.updateDatabase(['Me', 12, 33], True)
    print('Completed adding records!\n\n')
    input()

    # writer encrypt table test
    print('Encrypting table...')
    # curTime = time.time()
    writer.encrypt()
    input()

    # endTime = time.time()
    # delta = endTime - curTime
    # print(f"Time difference is {delta} seconds")
    print('Completed encrypting table!\n\n')
    
    # auth delegation
    print('Authorizing readers...')
    writer.delegate(reader.getPublicKey(), reader.id)
    print('Completed authorizing readers!\n\n')
    input()

    # search query
    print('Generating trapdoors...')
    trapdoors = reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';")
    print('Completed generating trapdoors!\n\n')
    input()

    print('Transforming trapdoors...')
    tPrime = qm.transform(trapdoors, reader.id)
    print('Completed transforming trapdoors!\n\n')
    input()

    print('Trapdoor search...')
    results = dh.search(tPrime)
    printResults(results, "SELECT * FROM Molecules WHERE BOND_NO='1';", reader.id)
    print('Completed trapdoor search!\n\n')
    input()


    # print('Generating second trapdoors...')
    # trapdoors2 = reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1' OR NAME='Earth';")
    # print('Completed generating second trapdoors!\n\n')

    # print('Transforming second trapdoors...')
    # tPrime2 = qm.transform(trapdoors2, reader.id)
    # print('Completed transforming second trapdoors!\n\n')
    
    # print('Second trapdoor search...')
    # results2 = dh.search(tPrime2)
    # printResults(results2, "SELECT * FROM Molecules WHERE BOND_NO='1' OR NAME='Earth';", reader.id)
    # print('Completed second trapdoor search!\n\n')

    # print('Generating bad trapdoor...')
    # badTrapdoor = reader2.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';")
    # print('Completed generating bad trapdoor!\n\n')

    # print('Transforming bad trapdoor...')
    # badTPrime = qm.transform(badTrapdoor, reader2.id)
    # print('Completed transforming bad trapdoor!\n\n')

    # print('Bad trapdoor search... (unauthorized Cathy searches)')
    # badResults = dh.search(badTPrime)
    # printResults(badResults, "SELECT * FROM Molecules WHERE BOND_NO='1';", reader2.id)
    # print('Completed bad trapdoor search!\n\n')


    qm.printData()



if __name__ == '__main__':
    # main()
    testScheme()

    