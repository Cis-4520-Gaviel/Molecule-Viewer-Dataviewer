from pymcl import pairing, Fr
from termcolor import colored
from DataHost import DataHost
class QueryMutliplexer():

    def _auth(self, readerId):
        print(colored('QM', 'green'),'\t checking if',colored(readerId,'cyan'),'is authorized...')
        authorizedWriters = []
        for writer in list(self._authorizations.keys()):
            if readerId in self._authorizations[writer]:
                authorizedWriters.append(writer)
                print(colored('QM', 'green'),'\t',colored(writer, 'cyan') ,' has authorized!',self._authorizations[writer])
        if not authorizedWriters:
            print(colored('QM', 'green'),'\t not authorized!')
            pass

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
        print(colored('QM', 'green'),'\t add writer [',colored(id, 'cyan'),'] with secret key [',symmetricKey,']')
        self._writers.append((id, symmetricKey))
        self._authorizations[id] = {}
        print(colored('QM', 'green'),'\t done add writer')

    def addReader(self, publicKey: Fr, id: str):
        print(colored('QM', 'green'),'\t add reader [',colored(id, 'cyan'),'] with public key [',publicKey,']')
        self._readers.append((id, publicKey)) #prob need to add more authentication still
        print(colored('QM', 'green'),'\t done add reader')
    
    def delegate(self, auth, writerId, readerId):
        print(colored('QM', 'green'),'\t',colored(writerId, ('cyan')),'authorizes',colored(readerId, 'cyan'), '[',auth,']')
        if writerId not in self._authorizations:
            return False
        self._authorizations[writerId][readerId] = auth # replace this with the actual value
        print(colored('QM', 'green'),'\t done delegate')
    
    def transform(self, trapdoor, readerId, dataHost : DataHost = None ):
        print(colored('QM - GET', 'green'),'\t transform trapdoor', trapdoor,'for',colored(readerId, 'cyan'))
        authR = self._auth(readerId=readerId)
        tPrimePrime = []

        for w in authR:
            tPrime = []
            for t in trapdoor:
                (pos, kW, tableName) = t
                # #print(tableName)
                # #print(pos.__class__)
                try:
                    cRSW = pairing(pos, self._authorizations[w][readerId])
                    tableName = pairing( tableName, self._authorizations[w][readerId])
                except:
                    continue
        
                #create zsgbf
                #oblivious transfer
                tPrime.append((cRSW, kW, tableName))
            tPrimePrime.append(tPrime)

        print(colored('QM', 'green'),'\t done transform',tPrimePrime)
        if(dataHost is None):
            return tPrimePrime
        
        ids, results = dataHost.search(tPrimePrime, readerId=readerId)
        print(colored('QM - RECIEVE', 'green'),'\t recieved searched results:',results)

        return ids, results
    
    def filter(self, results):
        yield Exception("not implemented yet")

    def printData(self):
        """Omega debug function"""
        print(colored('QM', 'green'),'\t #print data')
        print("writers: ", self._writers)
        print("readers: ", self._readers)
        print("Authorizations:")
        for writer in self._authorizations:
            print(writer, self._authorizations[writer])
            pass

