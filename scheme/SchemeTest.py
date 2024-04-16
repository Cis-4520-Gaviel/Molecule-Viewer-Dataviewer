from termcolor import colored
import sys
from users.Users import Writer, Reader
from pymcl import pairing, g1,g2
from database.QueryMultiplexer import QueryMutliplexer
from database.DataHost import DataHost
from database.EncryptedDatabase import EncryptedDatabase
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

def logAction(data, header):
    f = open("testEncryptDuration.txt", "a")
    dataString = header + "," + ",".join(data)
    f.write(dataString)
    f.write("\n")
    f.close()

def runMainScheme():
    
    # init QM and DH
    qm = QueryMutliplexer(b'123')
    dh = DataHost(EncryptedDatabase(True))

    # init writer and readers
    print('Initializing users...')
    writer = Writer(qm, dh, "Alice")
    writer2 = Writer(qm, dh, "Myron")
    print()
    reader = Reader(qm, dh, "Bob")
    print()
    reader2 = Reader(qm, dh, "Mallory")

    reader3 = Reader(qm, dh, "Eric")
    print('Completed initializing users!\n\n')
    input("Press enter to continue to next step")

    # table creation
    print('Adding records to db...')
    writer2.updateDatabase(['3-HeptaneOctone', 10, 3])
    writer2.updateDatabase(['4-3-redstoneheptane', 1, 1])
    writer.updateDatabase(['Fire', 1, 1])
    writer.updateDatabase(['Water', 2, 1])
    writer.updateDatabase(['Earth', 1, 3])
    writer.updateDatabase(['Joel', 69, 12])
    writer.updateDatabase(['Myron', 100, 11])
    writer.updateDatabase(['Me', 12, 33])
    for i in range(30):
        molName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        atomCount = random.randint(0,1000)
        bondCount = random.randint(0,30)
        writer.updateDatabase([molName, atomCount, bondCount ])
    print('Completed adding records!\n\n')
    input("Press enter to continue to next step")

    # writer encrypt table test
    print('Encrypting table...')
    curTime = time.time()
    writer.encrypt()
    endTime = time.time()
    delta = endTime - curTime
    logAction([str(delta)], "time for 10000 records")
    writer2.encrypt()

    # endTime = time.time()
    # delta = endTime - curTime
    # print(f"Time difference is {delta} seconds")
    print('Completed encrypting table!\n',delta,' Seconds elapsed to encrypt Alices Index\n')
    input("Press enter to continue to next step")
    
    # auth delegation
    print('Authorizing readers...')
    writer.delegate(reader.getPublicKey(), reader.id)
    writer.delegate(reader3.getPublicKey(), reader3.id)
    writer2.delegate(reader3.getPublicKey(), reader3.id)
    print('Completed authorizing readers!\n\n')
    print("Press enter to continue to next step")

    # search query

    while(True):
        print("""Enter test number to run:
1\tBob searches using 'SELECT * FROM Molecules WHERE BOND_NO='1';'
2\tBob searches using 'SELECT * FROM Molecules WHERE BOND_NO='1' OR NAME='Earth';'
3\tMallory searches using 'SELECT * FROM Molecules WHERE BOND_NO='1';'
4\tEric searches using 'SELECT * FROM Molecules WHERE BOND_NO='1';'
5\tEric searches using a custom SQL statement
exit\tClose Program""")
        userInput = input("Enter the number of the test to run\n")
        try:
            if(userInput == "exit"):
                break
            if(userInput == "1"):
                print('Generating trapdoors...')
                results = reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';")
                printResults(results, "SELECT * FROM Molecules WHERE BOND_NO='1';", reader.id)
                print('Completed trapdoor search!\n\n')
            if(userInput == "2"):

                print('Generating second trapdoors...')
                results = reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1' OR NAME='Earth';")
                printResults(results, "SELECT * FROM Molecules WHERE BOND_NO='1' OR NAME='Earth';", reader.id)
                print('Completed second trapdoor search!\n\n')
            if(userInput == "3"):

                print('Generating bad trapdoor...')
                results = reader2.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';")
                print('Completed generating bad trapdoor!\n\n')
                printResults(results, "SELECT * FROM Molecules WHERE BOND_NO='1';", reader2.id)
                print('Completed bad trapdoor search!\n\n')
            if(userInput == "4"):
                print('Generating trapdoors...')
                results = reader3.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';")
                printResults(results, "SELECT * FROM Molecules WHERE BOND_NO='1';", reader3.id)
                print('Completed trapdoor search!\n\n')
            if(userInput == "5"):
                print("Enter an SQL Statement that Eric enters")
                sqlStuff = input()
                results = reader3.trapdoor(sqlStuff)
                printResults(results, sqlStuff, reader3.id)
                print('Completed trapdoor search!\n\n')
        except Exception as error:
            print(error)
    qm.printData()

def testScheme2():
    qm = QueryMutliplexer(b'123')
    dh = DataHost(EncryptedDatabase(True))

    # init writer and readers
    print('Initializing users...')
    writer = Writer(qm, dh, "Alice")
    writer2 = Writer(qm, dh, "Myron")
    writer3 = Writer(qm, dh, "Eric")
    writer4 = Writer(qm, dh, "Me")
    print()
    reader = Reader(qm, dh, "Bob")
    print()
    reader2 = Reader(qm, dh, "Cathy")

    reader3 = Reader(qm, dh, "Eric")
    reader4 = Reader(qm, dh, "You")
    print('Completed initializing users!\n\n')
    input()

    writer.delegate(reader.getPublicKey(), reader.id)
    writer2.delegate(reader2.getPublicKey(), reader2.id)
    writer3.delegate(reader3.getPublicKey(), reader3.id)
    writer4.delegate(reader4.getPublicKey(), reader4.id)

    # table creation
    # print('Adding records to db...')
    # writer2.updateDatabase(['3-HeptaneOctone', 10, 3])
    # writer2.updateDatabase(['4-3-redstoneheptane', 1, 1])
    # writer.updateDatabase(['Fire', 1, 1])
    # writer.updateDatabase(['Water', 2, 1])
    # writer.updateDatabase(['Earth', 1, 3])
    timesRun = 1000
    records = [[],[],[]]
    for i in range(timesRun):
        molName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        atomCount = random.randint(0,1000)
        bondCount = random.randint(0,30)
        writer.updateDatabase([molName, atomCount, bondCount ], True)
        curTime = time.time()
        reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1';")
        endTime = time.time()
        delta = endTime - curTime
        records[0].append(str(delta))

        curTime = time.time()
        reader.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1' OR NAME='AEA';")
        endTime = time.time()
        delta = endTime - curTime
        records[1].append(str(delta))

        curTime = time.time()
        reader.trapdoor("SELECT * FROM Molecules WHERE NAME='AEAA';")
        endTime = time.time()
        delta = endTime - curTime
        records[2].append(str(delta))
    
    logAction(records[0], "search single")
    logAction(records[1], "search multiple")
    logAction(records[2], "search none")

    # records = []
    # for i in range(timesRun):
    #     molName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    #     atomCount = random.randint(0,1000)
    #     bondCount = random.randint(0,30)
    #     writer2.updateDatabase([molName, atomCount, bondCount ], True)

    #     curTime = time.time()
    #     reader2.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1' OR NAME='AEA';")
    #     endTime = time.time()
    #     delta = endTime - curTime
    #     records.append(str(delta))
    
    # logAction(records, "search multiple")

    # records = []
    # for i in range(timesRun):
    #     molName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    #     atomCount = random.randint(0,1000)
    #     bondCount = random.randint(0,30)
    #     writer3.updateDatabase([molName, atomCount, bondCount ], True)
    #     curTime = time.time()
    #     reader3.trapdoor("SELECT * FROM Molecules WHERE NAME='AEAA';")
    #     endTime = time.time()
    #     delta = endTime - curTime
    #     records.append(str(delta))
    
    # logAction(records, "search none")

    records = []
    for i in range(timesRun):
        molName = random.choice('abc')
        atomCount = random.randint(0,1000)
        bondCount = random.randint(0,30)
        writer4.updateDatabase([molName, atomCount, bondCount ], True)
        curTime = time.time()
        reader4.trapdoor("SELECT * FROM Molecules WHERE BOND_NO='1' OR NAME='c';")
        endTime = time.time()
        delta = endTime - curTime
        records.append(str(delta))
    
    logAction(records, "search a lot")

def testScheme3():
        # init
    # print(g1)
    # print(g1)

    
    # init QM and DH
    qm = QueryMutliplexer(b'123')
    dh = DataHost(EncryptedDatabase(True))

    # init writer and readers
    print('Initializing users...')
    writer = Writer(qm, dh, "Alice")
    writer2 = Writer(qm, dh, "Myron")
    print()
    reader = Reader(qm, dh, "Bob")
    print()
    reader2 = Reader(qm, dh, "Mallory")

    reader3 = Reader(qm, dh, "Eric")
    print('Completed initializing users!\n\n')
    input()

    # table creation
    print('Adding records to db...')
    # writer2.updateDatabase(['3-HeptaneOctone', 10, 3])
    # writer2.updateDatabase(['4-3-redstoneheptane', 1, 1])
    # writer.updateDatabase(['Fire', 1, 1])
    # writer.updateDatabase(['Water', 2, 1])
    # writer.updateDatabase(['Earth', 1, 3])
    # records = []
    # for i in range(100):
    #     molName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    #     atomCount = random.randint(0,1000)
    #     bondCount = random.randint(0,30)
    #     writer.updateDatabase([molName, atomCount, bondCount ])
    #     curTime = time.time()
    #     writer.encrypt()
    #     endTime = time.time()
    #     delta = endTime - curTime
    #     records.append(str(delta))
    
    # logAction(records, "encrypt index only")
    # records = []
    # for i in range(100):
    #     molName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    #     atomCount = random.randint(0,1000)
    #     bondCount = random.randint(0,30)
    #     curTime = time.time()
    #     writer2.updateDatabase([molName, atomCount, bondCount ], True)
    #     endTime = time.time()
    #     delta = endTime - curTime
    #     records.append(str(delta))
    
    # logAction(records, "add then encrypt")

    # records = []
    # for i in range(100):
    #     molName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
    #     atomCount = random.randint(0,1000)
    #     bondCount = random.randint(0,30)
    #     writer3.updateDatabase([molName, atomCount, bondCount ])
    #     curTime = time.time()
    #     writer3.encrypt()
    #     endTime = time.time()
    #     delta = endTime - curTime
    #     records.append(str(delta))
    
    # logAction(records, "encryption time, 100 long molecule name")




if __name__ == '__main__':
    runMainScheme()

    