

# Constructs a dictionary W from database D
def CreateDictionary(D):
    table = D.retrieve_all('Molecules')
    allAttributes = D.getAttributes()
    W = {}
    # print('Total Attr:', allAttributes)
    # print()
    for k, v in W.items():
        print(k, v)
    id=1
    for record in table:
        i=0
        # print('cur record:', record)
        for attribute in allAttributes:
            # print('cur attr:', attribute)
            keyword = attribute + '=\'' + str(record[i]) + '\'' # create keyword from record
            if keyword in W:
                W[keyword].append(id) # add to id list of keyword
            else:
                W[keyword]=[id] # create new id list for keyword
            # Use .append
            id=id+1
            i=i+1
            # print(W)
        # print()
    # print('W')
    # print(W)
    return W, id-1

# Retrieves keyword from id
def GetKeyAtValue(W, id):
    for idlist in W.values():
        # find keyword with corresponding id
        if id in idlist:
            return list(W.keys())[list(W.values()).index(idlist)] # return keyword of id


