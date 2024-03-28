import sqlparse
from CryptoUtils import AESSIVEncryptNonce, phiFunction, get_xor
import os

def ExtractKeywords(sql):
    # print(sql)
    output = sqlparse.format(sql, reindent=True)
    # print(output)
    tokens = sqlparse.parse(sql)
    print(tokens[0].tokens)
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
            print("output: ",temp)
            print("comparisons:", temp.split("AND"))
            return temp.split("AND")
            # nextToken = token.token_next(1)
            # print('Occurrances',nextToken)
            # print(nextToken[1])
            # print("JALSDJFLKAJD")
        # print("\nstuff", token)

def generateTrapdoor(sql, K):
    keywords = ExtractKeywords(sql)
    # AESSIVEncryptNonce(K, keywords[0])
    trapdoors = []
    for keyword in keywords:
        pos = keyword
        kW = phiFunction(K, keyword)
        trapdoors.append((pos, kW.hex()))
    return trapdoors
    


if __name__ == "__main__":
        key = os.urandom(16)
        t = generateTrapdoor("""SELECT * FROM PATIENT WHERE Name='Mary' AND Surname='Grant';""" , key)
        t2 = generateTrapdoor("""SELECT * FROM PATIENT WHERE Name='Mary';""" , key)
        print('trapdoor', t)
        print('second trapdoor', t2)
    
