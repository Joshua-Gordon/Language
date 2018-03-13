
keywords = ["let","type","impure","import","from","in","macro","do","where","for","while","if","else"]
operators = [":","=","==","+","-","*","\\","/","%","&&","&","||","|","->","^","**","!","(",")","$",";","/*","//","*/","<",">","<=",">=",".","'",'"']
#TODO: Handle constants, floating point numbers, newlines

def readFile(f):
    with open(f) as file:
        return file.read()

def tokenize(s,mode, tokenList = []):
    if len(s) == 0:
        return tokenList
    #print(s,tokenList)
    def grabAlphanumeric(s):
        def grabAlphanumericHelper(s,done): #clobbers input until alphanumeric
            if len(s) == 0:
                return None
            if s[0].isalnum():
                try:
                    return str(s[0]) + str(grabAlphanumericHelper(s[1:],True))
                except:
                    return str(s[0])
            else:
                if not done:
                    return grabAlphanumericHelper(s[1:],False)
                return ""
        return grabAlphanumericHelper(s,False)
    def grabSymbol(s):
        def grabSymbolHelper(s): #clobbers input until symbol
            if len(s) == 0:
                return None
            if s[0] in operators:
                if s[:2] in operators:
                    return s[:2]
                else:
                    return s[0]
            else:
                return grabSymbolHelper(s[1:])
        return grabSymbolHelper(s)
    
    if mode == "identifier":
        token = grabAlphanumeric(s)
        if token in keywords:
            return (token, "keyword")
        else:
            return (token, "identifier")
    if mode == "operator":
        token = grabSymbol(s)
        return (token, "operator")
    if mode == "all":
        s = s.replace('\r','')
        s = s.replace('\n',';')
        ls = tokenList
        tokenA = grabAlphanumeric(s)
        tokenO = grabSymbol(s)
        #print("tokenA = ",tokenA)
        #print("tokenO = ",tokenO)
        trimmed = s.strip()
        #print(trimmed)
        if not tokenA == None and trimmed.startswith(tokenA):
            if tokenA in keywords:
                ls.append((tokenA,"keyword"))
            else:
                ls.append((tokenA,"identifier"))
            l = len(tokenA)
            return tokenize(trimmed[l:],"all",tokenList=ls)
        elif not tokenO == None and trimmed.startswith(tokenO):
            ls.append((tokenO,"operator"))
            l = len(tokenO)
            return tokenize(trimmed[l:],"all",tokenList=ls)
        else:
            return tokenize(trimmed[1:],"all",tokenList=ls)

def printTokens(tokenList):
    strings = list(map(lambda t: t[0] + " ",tokenList))
    return ''.join(strings)

def refineTokens(tokenList): #goes through a list of identifiers, keywords, and operators, and outputs a list of identifiers, keywords, operators, and literals (int literal, lambda, etc.)
    def isSequence(idx,tokens):
        #Checks if a sequence of tokens is present at an index.
        #If t[0] is None, then all values are matched
        for i in range(idx,idx+len(tokens)):
            t = tokens[i-idx]
            if t[0] == None:
                if tokenList[i][1] == t[1]:
                    pass
                else:
                    return False
            else:
                if tokenList[i] == t:
                    pass
                else:
                    return False
        return True
            

    def isNumeric(token):
        if token[1] == "identifier":
            if (""+token[0]).isdigit():
                return True

        return False

    def isFloat(idx): #index in tokenList
        if isNumeric(tokenList[idx]) and tokenList[idx+1] == (".","operator") and isNumeric(tokenList[idx+2]):
            return True
        return False

    def isLambda(idx): #Tells if there is a lambda header at this point in the token list
        if tokenList[idx] == ("\\","operator"):
                 while not tokenList[idx][0] == "->":
                     idx+=1
                     if not tokenList[idx][1] == "identifier":
                         return False
                 return (True,idx)
        return False

    def isTExpression(idx): #Tells if T expression header
        if isSequence(idx, [("T","identifier"),("<","operator")]):
                     return True
        return False

    def isString(idx):
        if tokenList[idx] == ('"',"operator"):
            i = idx+1
            try:
                while not tokenList[i] == ('"',"operator"):
                    i+=1
            except:
                return False
            return (True,i-idx)
        return False

    def isNewline(idx):
        return tokenList[idx] == (";","operator")
    
    newTokenList = []
    i = 0
    while i < len(tokenList):
        if isFloat(i):
                i+=3
                flt = ''.join(list(map(lambda s: s[0],tokenList))[i-3:i])
                print(flt)
                newTokenList.append((flt,"float"))
        elif isNumeric(tokenList[i]):
                num = tokenList[i][0]
                newTokenList.append((num,"integer"))
                i+=1
        elif not isString(i) == False:
                strlen = isString(i)[1]
                string = ''.join(list(map(lambda s: s[0],tokenList))[i+1:i+strlen])
                newTokenList.append((string,"string"))
                i +=2+strlen
        elif not isLambda(i) == False: #Please forgive me, but this is necessary
                l = isLambda(i)
                i = l[1]
                newTokenList.append((l[0],"lambda header"))
        elif isTExpression(i):
                i+=2
                TExp = ''.join(list(map(lambda s: s[0],tokenList))[i-2:i])
                newTokenList.append((TExp,"t header"))
        elif isNewline(i):
                i+=1
                newTokenList.append(("\n","newline"))
        else:
                newTokenList.append(tokenList[i])
                i+=1
    return newTokenList
            
        

    
    
