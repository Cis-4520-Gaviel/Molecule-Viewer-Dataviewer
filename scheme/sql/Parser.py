import sqlparse
def getNextNonWhitespaceToken(token, i, at = 0):
    # print("finding next token after", str(getTokenAtIndex(token, at)))
    while (token.token_next(i, skip_ws=False)[1] is not None):
        i = i + 1
        curToken = token.token_next(i, skip_ws=True)[1]
        # print("[curToken]: ", str(curToken), "[true token]: '", str(getTokenAtIndex(token, i)), "'")
        if(str(curToken) != str(token.token_next(at, skip_ws=False))):
            while(str(curToken) == str(getTokenAtIndex(token, i, skip_ws=True))):
                i = i + 1
            #     print("increase")
            # print("finished:", i, str(getTokenAtIndex(token, i, skip_ws=True)))
            return i - 1
        i = i + 1
    return -i
    
def getTokenAtIndex(token, i, skip_ws = False):
    return token.token_next(i, skip_ws=skip_ws)[1]

def getNonWhitespaceTokens(tokens):
    arr = []
    for tok in tokens:
        # print(str(tok), ":" , tok.ttype)
        if(tok.ttype == sqlparse.tokens.Whitespace):
            continue
        if(tok.ttype == None):
            arr.extend(getNonWhitespaceTokens(tok.tokens))
        else:
            arr.append(tok)
    return arr


def getSelectKeywords(sql):
    """
    This basically extracts the search keywords out of an sql statement. 
    DO NOT supply statements which do not contain statements. There is no error handling currently
    """

    # print(sql)
    output = sqlparse.format(sql, reindent=True)
    # print(output)
    tokens = sqlparse.parse(sql)
    # print('Tokens:',tokens[0].tokens)
    for token in tokens[0].tokens:
        if(isinstance(token, sqlparse.sql.Where)):
            temp = ""
            token2 = token
            i = 1
            while(token2.token_next(i, skip_ws=False)[1] is not None):
                curToken = token2.token_next(i, skip_ws=False)[1]
                # print(curToken, curToken.ttype, curToken.value, curToken.__class__)
                # if isinstance(curToken, sqlparse.sql.Identifier) or isinstance(curToken, sqlparse.sql.Token):
                if str(curToken) != " " and str(curToken) != ";":
                    temp += str(curToken)
                        
                i = i + 1
            # print(token.token_next(1)[1])
            # print("output: ",temp)
            # print("comparisons:", temp.split("AND"))
            return temp.split("AND")
            # nextToken = token.token_next(1)
            # print('Occurrances',nextToken)
            # print(nextToken[1])
            # print("JALSDJFLKAJD")
        # print("\nstuff", token)

def parseCreateStatement(sqlStatement):
    # print(sqlStatement)
    sections = sqlparse.format(sqlStatement, reindent=True, keyword_case='upper')
    # for thing in sections:
    #     print(thing)
    # print(sections)
    tokens = sqlparse.parse(sqlStatement)
    # print(tokens[0])
    # for token in tokens[0]:
    #     print(token)
    # print(tokens[0].tokens)
    token = tokens[0]
    i = 1
    stage = 1
    tableName = ""
    tableAttributes = []
    while (token.token_next(i, skip_ws=False)[1] is not None):
        curToken = token.token_next(i, skip_ws=False)[1]
        i = i+1
        if (curToken.ttype == sqlparse.tokens.Whitespace or curToken.ttype == sqlparse.tokens.Newline):
            continue

        if(stage == 1): # retrieve table name
            if(str(curToken) != "TABLE"):
                continue
            tableNameIdx = i
            
            while(True):
                newIndex = getNextNonWhitespaceToken(token, tableNameIdx, i)
                tableNameIdx = newIndex
                if(getTokenAtIndex(token, tableNameIdx, skip_ws=True).ttype == None): # identifier found
                    break
            
            tableName = str(getTokenAtIndex(token, tableNameIdx, skip_ws=True))
            i = tableNameIdx + 1
            stage = 2
            continue
        
        elif (stage == 2): # retrieve attributes
            if(curToken.ttype != None):
                continue
            # print(str(curToken), curToken.tokens, i)
            attributeList = getNonWhitespaceTokens(curToken)
            
            for tok in attributeList:
                if(tok.ttype == sqlparse.tokens.Name):
                    tableAttributes.append(str(tok))
            stage = 3

    print("table:",tableName)
    print("attributes:",tableAttributes)

def parseInsertStatement(sqlStatement):
    # print(sqlStatement)
    sections = sqlparse.format(sqlStatement, reindent=True, keyword_case='upper')
    # for thing in sections:
    #     print(thing)
    # print(sections)
    tokens = sqlparse.parse(sqlStatement)
    # print(tokens[0])
    # for token in tokens[0]:
    #     print(token)
    # print(tokens[0].tokens)
    token = tokens[0]
    i = 1
    stage = 1
    tableName = ""
    tableAttributes = []
    while (token.token_next(i, skip_ws=False)[1] is not None):
        curToken = token.token_next(i, skip_ws=False)[1]
        i = i+1
        if (curToken.ttype == sqlparse.tokens.Whitespace or curToken.ttype == sqlparse.tokens.Newline):
            continue

        if(stage == 1): # retrieve table name
            if(str(curToken) != "INTO"):
                continue
            tableNameIdx = i
            
            while(True):
                newIndex = getNextNonWhitespaceToken(token, tableNameIdx, i)
                tableNameIdx = newIndex
                if(getTokenAtIndex(token, tableNameIdx, skip_ws=True).ttype == None): # identifier found
                    break
            # print(getTokenAtIndex(token, tableNameIdx, skip_ws=True).tokens)
            tableName = str(getTokenAtIndex(token, tableNameIdx, skip_ws=True).tokens[0])
            i = tableNameIdx + 1
            stage = 2
            continue
        
        elif (stage == 2): # retrieve values
            if(curToken.ttype != None):
                continue
            # print(str(curToken), curToken.tokens, i)
            attributeList = getNonWhitespaceTokens(curToken.tokens)
            # print(attributeList)
            onlyValues = attributeList[2:-1] # remove VALUES ( ) from the array
            # print(onlyValues)
            for tok in onlyValues:
                if(tok.ttype != sqlparse.tokens.Punctuation):
                    # print(dir(tok))
                    tableAttributes.append(tok.value)
            stage = 3

        # print(curToken, curToken.ttype)
    print("table:",tableName)
    print("values:",tableAttributes)

if __name__ == "__main__":
    parseCreateStatement("""CREATE TABLE IF NOT EXISTS Molecules 
                        (   NAME            TEXT            NOT NULL,
                            ATOM_NO         INTEGER         NOT NULL,
                            BOND_NO         INTEGER         NOT NULL);""")
    parseCreateStatement("""CREATE TABLE   Molecules 
                        (   NAME            TEXT            NOT NULL,
                            ATOM_NO         INTEGER         NOT NULL,
                            BOND_NO         INTEGER         NOT NULL);""")
    parseInsertStatement("""INSERT OR IGNORE
                            INTO Molecules (NAME, ATOM_NO, BOND_NO)
                            VALUES ('Fire', 1, 2)""")                     
    parseInsertStatement("""INSERT OR IGNORE
                            INTO Molecules (NAME, ATOM_NO, BOND_NO)
                            VALUES ('Fire balls', 1, 2)""")                     