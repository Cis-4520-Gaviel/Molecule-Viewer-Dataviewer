class Node:
    def __init__(self, unencryptedString):
        args = unencryptedString.split(" ")
        if (args.length() != 3):
            raise Exception("bad")
        self.recordID = args[0]
        self.kNext = args[1]
        self.addressNext = args[2]
    
    def __init__(self, recordID, kNext, addressNext):
        self.recordID = recordID
        self.kNext = kNext
        self.addressNext = addressNext
    
    def setNextAddress(self, addressNext):
        self.addressNext = addressNext
    
    def __str__(self):
        return f"{self.recordID} {self.kNext} {self.addressNext}"