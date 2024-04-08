

# Constructs a dictionary W from database D
def CreateDictionary(D, tableName: str):
    """
    Generates the dictionary of keywords of a given table.
    To be used for BuildIndex
    """
    table = D.retrieve_all(tableName)
    allAttributes = D.getAttributes()
    W = {}

    for k, v in W.items():
        #print(k, v)
        pass
    id=1
    for record in table:
        i=0
        for attribute in allAttributes:
            # #print('cur attr:', attribute)
            keyword = attribute + '=\'' + str(record[i]) + '\'' # create keyword from record
            if keyword in W:
                W[keyword].append(id) # add to id list of keyword
            else:
                W[keyword]=[id] # create new id list for keyword
            # Use .append
            i=i+1

        id=id+1
    return W, id-1

# Retrieves keyword from id
def GetKeyAtValue(W, id):
    for idlist in W.values():
        # find keyword with corresponding id
        if id in idlist:
            return list(W.keys())[list(W.values()).index(idlist)] # return keyword of id


