from pymcl import pairing, Fr
class QueryMutliplexer():

    def _auth(self, readerId):
        print('QM: checking if',readerId,'is authorized...')
        authorizedWriters = []
        for writer in list(self._authorizations.keys()):
            if readerId in self._authorizations[writer]:
                authorizedWriters.append(writer)
                print('QM: authorized!',self._authorizations[writer])
        if not authorizedWriters:
            print('QM: not authorized!')

        return authorizedWriters

    def __init__(self, masterKey):
        self.masterKey = masterKey # idk where we use this lol
        self._writers = []
        self._readers = []
        self._authorizations = {}

    def addWriter(self, symmetricKey: Fr, id):
        """
        Add a given writer from their id and symmetric key
        """
        print('QM: add writer [',id,'] with secret key [',symmetricKey,']')
        self._writers.append((id, symmetricKey))
        self._authorizations[id] = {}
        print('QM: done add writer')

    def addReader(self, publicKey: Fr, id: str):
        print('QM: add reader [',id,'] with public key [',publicKey,']')
        self._readers.append((id, publicKey)) #prob need to add more authentication still
        print('QM: done add reader')
    
    def delegate(self, auth, writerId, readerId):
        print('QM:',writerId,'authorizes',readerId, '[',auth,']')
        if writerId not in self._authorizations:
            return False
        self._authorizations[writerId][readerId] = auth # replace this with the actual value
        print('QM: done delegate')
    
    def transform(self, trapdoor, readerId):
        print('QM: transform trapdoor', trapdoor,'for',readerId)
        authR = self._auth(readerId=readerId)
        tPrime = []

        for t in trapdoor:
            (pos, kW, tableName) = t
            for w in authR:
                # print(pos.__class__)
                cRSW = pairing(pos, self._authorizations[w][readerId])
                tableName = pairing(tableName, self._authorizations[w][readerId])
                #create zsgbf
                #oblivious transfer
                tPrime.append((cRSW, kW, tableName))

        print('QM: done transform',tPrime)
        return tPrime
    
    def filter(self, results):
        yield Exception("not implemented yet")

    def printData(self):
        """Omega debug function"""
        print('QM: print data')
        print("writers: ", self._writers)
        print("readers: ", self._readers)
        print("Authorizations:")
        for writer in self._authorizations:
            print(writer, self._authorizations[writer])

