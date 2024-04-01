from pymcl import pairings
class QueryMutliplexer():

    def _auth(self, readerId):
        authorizedWriters = []
        for writer in list(self.__authorizations.keys()):
            if readerId in self.__authorizations[writer]:
                authorizedWriters.append(writer)
        
        return authorizedWriters

    def __init__(self, masterKey):
        self.masterKey = masterKey # idk where we use this lol
        self.__writers = []
        self.__readers = []
        self.__authorizations = {}

    def addWriter(self, id, symmetricKey):
        self.__writers.append((id, symmetricKey))
        self.__authorizations[id] = []

    def addReader(self, id, publicKey, privateKey):
        self.__readers.append((id, publicKey)) #prob need to add more authentication still
    
    def delegate(self, writerId, readerId):
        if writerId not in self.__authorizations:
            return False
        self.__authorizations[writerId][readerId] = True # replace this with the actual value
    
    def transform(self, trapdoor, readerId):
        authR = self._auth(readerId=readerId)
        for w in authR:
            cRSW = pairings(trapdoor, self.__readers[readerId] * w)
        return True