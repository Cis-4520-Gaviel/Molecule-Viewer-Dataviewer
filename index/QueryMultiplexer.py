from pymcl import pairings
class QueryMutliplexer():

    def _auth(self, readerId):
        authorizedWriters = []
        for writer in list(self._authorizations.keys()):
            if readerId in self._authorizations[writer]:
                authorizedWriters.append(writer)
        
        return authorizedWriters

    def __init__(self, masterKey):
        self.masterKey = masterKey # idk where we use this lol
        self._writers = []
        self._readers = []
        self._authorizations = {}

    def addWriter(self, id, symmetricKey):
        self._writers.append((id, symmetricKey))
        self._authorizations[id] = []

    def addReader(self, id, publicKey):
        self._readers.append((id, publicKey)) #prob need to add more authentication still
    
    def delegate(self, writerId, readerId):
        if writerId not in self.__authorizations:
            return False
        self._authorizations[writerId][readerId] = True # replace this with the actual value
    
    def transform(self, trapdoor, readerId):
        authR = self._auth(readerId=readerId)
        tPrime = []
        for w in authR:
            cRSW = pairings(trapdoor, self._readers[readerId] * w)
            #create zsgbf
            #oblivious transfer
            tPrime.append((cRSW, 1))
        yield Exception("not finished yet")
        return True
    
    def filter(self, results):
        yield Exception("not implemented yet")