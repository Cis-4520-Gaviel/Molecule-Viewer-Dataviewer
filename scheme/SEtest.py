from database.Database import *
from utils.KeyGen import *
from database.CreateDictionary import *
from database.BuildIndex import *
from users.Trapdoor import *
from database.Search import *
from pymcl import Fr


# Create test database
D = Database(reset=True)
D.create_tables()
D.conn.execute( """INSERT
                    INTO Molecules (NAME,  ATOM_NO,    BOND_NO)
                    VALUES ('Fire', 1, 1);""" )
D.conn.execute( """INSERT
                    INTO Molecules (NAME,  ATOM_NO,    BOND_NO)
                    VALUES ('Water', 2, 1);""" )
D.conn.execute( """INSERT
                    INTO Molecules (NAME,  ATOM_NO,    BOND_NO)
                    VALUES ('Snow', 3, 2);""" )
print('Dataset:', D.retrieve_all('Molecules'))

# Create keys
Klen = 256
K = KeyGen(Klen) # K = (Kpsi, Kpi, Kphi)
sK = Fr.random()

privKey = Fr.random()
# Test CreateDictionary
print('Testing CreateDictionary...')
W, n = CreateDictionary(D, 'Molecules')
print(W)
# print('Indexing...')
# for i in range(1, n+1):
#     key = GetKeyAtValue(W, i)
#     print(key)
print('Completed CreateDictionary!\n\n')


# Test BuildIndex
print('Testing BuildIndex...')
I = BuildIndex(W,n,K,Klen, sK)
# print(I)
# (A,T) = I
# print('A:')
# print(A)
# print('table (values will appear different because of XOR):')
# print(T)
print('Completed BuildIndex!\n\n')


# Test Trapdoor
print('Testing Trapdoor...')
# Example SQL statements (only uncomment one)
# sql = """SELECT * FROM Molecules WHERE NAME='Fire';"""
# sql = """SELECT * FROM Molecules WHERE NAME='Water';"""
# sql = """SELECT * FROM Molecules WHERE NAME='Snow';"""
sql = """SELECT * FROM Molecules WHERE BOND_NO='1';"""
minecraftdoor = generateTrapdoor(sql,privKey)
print(minecraftdoor)
print('Completed Trapdoor!\n\n')


# Test Search
print('Testing Search...')
R = Search(I,minecraftdoor)
print('retrieved record ids:',R)
print('Completed Search!\n\n')


