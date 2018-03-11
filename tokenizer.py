
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
    def isNumeric(token):
        if token[1] == "identifier":
            if token[0].isdigit():
                return True

        return False

    def isFloat(idx): #index in tokenList
        if isNumeric(tokenList[idx] and tokenList[idx+1] == (".","operator") and isNumeric(tokenList[idx+2]):
            return True

    def isLambda(idx): #Tells if there is a lambda header at this point in the token list
        if tokenList[idx] == ("\\","operator"):
                 while not tokenList[idx][0] == "->":
                     idx+=1
                     if not tokenList[idx][1] == "identifier":
                         return False
                 return True   



    
    
