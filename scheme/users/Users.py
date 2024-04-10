import os
from pymcl import Fr, g1, g2, pairing
from abc import ABC, abstractmethod

from termcolor import colored
from users.Trapdoor import generateTrapdoor
from database.QueryMultiplexer import QueryMutliplexer
from database.DataHost import DataHost
from KeyGen import KeyGen
from database.Database import Database
from sql.Parser import parseInsertStatement
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
from utils.CryptoUtils import AESSIVDecryptNonce
from utils.Records import convertStringToTuple

class User(ABC):
    @abstractmethod
    def _setup(self):
        pass

    def __init__(self, queryMultiplexer : QueryMutliplexer, dataHost: DataHost, id: str):
        self.QM = queryMultiplexer
        self.DH = dataHost
        self.id = id

class Writer(User):
    """
    Writer user that interacts with the Gaviel scheme. Contains a single symmetric key
    Has the ability to delegate authorizations to readers, and encrypt a database
    """
    def _setup(self):
        secretKey = Fr.random()
        self._keySet = KeyGen(256)
        return secretKey

    def __init__(self, queryMultiplexer, dataHost, id):
        print('New Writer:', colored(id, 'cyan'))

        self._secretKey = self._setup()
        print(colored('Writer', 'green'),'\t gen secret key [',self._secretKey,']')

        self._database = Database(id,True)
        self._database.create_tables()
        super().__init__(queryMultiplexer, dataHost, id)

        self.QM.addWriter(self._secretKey, self.id)

        self.createNewTable('Molecules', ['NAME', 'ATOM_NO', 'BOND_NO'])
        
    def createNewTable(self, tableName, attributes):
        print(colored('Writer', 'green'),'\t create new table [',colored(tableName, 'yellow'),'] with attributes',attributes)

        encTableName = pairing(g1.hash(bytes(tableName, 'utf-8')), g2 * self._secretKey)
        self.DH.registerNewTable(encTableName.serialize().hex(), attributes)

        print(colored('Writer', 'green'),'\t done create table')

    def updateDatabase(self, values, rebuildIndex = False, tableName = "Molecules"):
        print(colored('Writer', 'green'),'\t update database with attributes',values)

        self._database.add_molecule(*values)
        encTableName = pairing(g1.hash(bytes(tableName, 'utf-8')), g2 * self._secretKey)
        self.DH.addNewValuesToTable(encTableName.serialize().hex(), values)

        if(rebuildIndex == True):
            self.encrypt('Molecules')
        print(colored('Writer', 'green'),'\t done update database')

    def delegate(self, readerPublicKey: Fr, readerId: str):
        """
        Authorize a reader via their public key
        """
        print(colored('Writer', 'green'),'\t authorize reader [',colored(readerId, 'cyan'),'] with pub key [',readerPublicKey,']')

        auth = readerPublicKey * self._secretKey
        self.QM.delegate(auth, self.id, readerId)

        print(colored('Writer', 'green'),'\t done authorize reader')

    def encrypt(self, tableName = 'Molecules'):
        """
        Generates an encrypted index for a given table that the writer owns.
        """
        print(colored('Writer', 'green'),'\t encrypt table')
        encTableName = pairing(g1.hash(bytes(tableName, 'utf-8')), g2 * self._secretKey)
        self.DH.encryptTable(self._database, encTableName.serialize().hex(), self._keySet, secretKey=self._secretKey, realTableName=tableName)
        print(colored('Writer', 'green'),'\t done encrypt table')

    def encryptKeyword(self, keyword):
        return pairing(g1.hash(bytes(keyword, 'utf-8')), g2 * self._secretKey)
    #database

class Reader(User):
    """
    A reader user in the Gaviel scheme. Has a pair of private and public keys, as well as
    a symmetric key for transforming their search queries (trapdoors)
    """
    def _setup(self):
        privateKey = Fr.random()
        publicKey = g2 * ~privateKey
        kR = AESSIV.generate_key(256)
        return publicKey, privateKey, kR

    def __init__(self, queryMultiplexer, dataHost, id):
        print('New Reader:',colored(id, 'cyan'))

        publicKey, privateKey, kR = self._setup()

        self._publicKey = publicKey
        self._privateKey = privateKey
        self._kR = kR

        print(colored('Reader', 'green'),'\t gen public key [',self._publicKey,']')
        print(colored('Reader', 'green'),'\t gen private key [',self._privateKey,']')
        
        super().__init__(queryMultiplexer, dataHost, id)
        self.QM.addReader(self._publicKey, self.id)
        self.DH.addReader(self.id, self._kR)

    def getPublicKey(self) -> Fr:
        print("Reader: get pub key [",self._publicKey,']')
        return self._publicKey
    
    def trapdoor(self, sqlStatement):
        """
        Generate and send a trapdoor to the QM. Performs a search within the encrypted database.
        Returns the record ids of the database, and correponding record ids.
        The set of ids will not be adjusted if there are duplicate ids when searching different writer's databases.
        """
        print(colored('Reader', 'green'),'\t generate trapdoor for [',colored(sqlStatement, 'yellow'),'] using priv key')
        t = generateTrapdoor(sqlStatement, self._privateKey) 
        print(colored('Reader - POST', 'green'),'\t done generate trapdoor, sending to QM: ', t)
        ids, trapdoors = self.QM.transform(t, self.id, self.DH)
        decryptedTrapdoors = []
        for t in trapdoors:
            plaintext = AESSIVDecryptNonce(self._kR, t).decode('utf-8')
            decryptedTrapdoors.append(convertStringToTuple(plaintext))
        
        return ids, decryptedTrapdoors
