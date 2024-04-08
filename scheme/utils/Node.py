class Node:
    def parseString(unencryptedString):
        args = unencryptedString.split(" ")
        # print(args)
        if (len(args) != 3):
            raise Exception("bad")
        if(args[2] == "None"):
            addressNext = None
        else:
            addressNext = int(args[2]) 
        return Node(int(args[0]), bytes.fromhex(args[1]), addressNext)
    
    def __init__(self, recordID: int, kNext: bytes, addressNext: int):
        self.recordID = recordID
        self.kNext = kNext
        self.addressNext = addressNext
    
    def setNextAddress(self, addressNext):
        self.addressNext = addressNext
    
    def __str__(self):
        return f"{self.recordID} {self.kNext.hex()} {self.addressNext}"