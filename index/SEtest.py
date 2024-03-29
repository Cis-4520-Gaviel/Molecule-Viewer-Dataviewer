from Database import *
from KeyGen import *
from CreateDictionary import *
from BuildIndex import *
from Trapdoor import *
from Search import *

# Create test database
D = Database(reset=True)
D.create_tables()
D.conn.execute( """INSERT
                    INTO Molecules (NAME,  ATOM_NO,    BOND_NO)
                    VALUES ('Fire', 1, 1);""" )
# db.conn.execute( """INSERT
#                     INTO Molecules (NAME,  ATOM_NO,    BOND_NO)
#                     VALUES ('Water', 2, 1);""" )
# db.conn.execute( """INSERT
#                     INTO Molecules (NAME,  ATOM_NO,    BOND_NO)
#                     VALUES ('Snow', 3, 2);""" )
# print('Dataset:', db.retrieve_all('Molecules'))

# Create keys
Klen = 256
K = KeyGen(Klen) # K = (Kpsi, Kpi, Kphi)

# Test CreateDictionary
print('Testing CreateDictionary...')
W, n = CreateDictionary(D)
print(W)
# print('Indexing...')
# for i in range(1, n+1):
#     key = GetKeyAtValue(W, i)
#     print(key)
print('Completed CreateDictionary!\n\n')


# Test BuildIndex
print('Testing BuildIndex...')
I = BuildIndex(W,n,K,Klen)
# print(I)
print('Completed BuildIndex!\n\n')


# Test Trapdoor
print('Testing Trapdoor...')
# An example SQL statement
minecraftdoor = generateTrapdoor("""SELECT * FROM Molecules WHERE NAME='Fire';""",K)
print(minecraftdoor)
print('Completed Trapdoor!\n\n')


# Test Search
print('Testing Search...')
Q = Search(I,minecraftdoor)
print('Completed Search!\n\n')


