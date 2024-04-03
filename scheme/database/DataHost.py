class DataHost:
    def __init__(self) -> None:
        self._readerKeys = {}
        pass

    def process(self, trapdoors):
        pass

    def readerKeygen(self, readerId, readerKey):
        self._readerKeys[readerId] = readerKey