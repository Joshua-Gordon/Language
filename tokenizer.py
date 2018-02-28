
keywords = ["let","type","impure","import","from","in","macro","do","where","for","while","if","else"]
operators = [":","=","==","+","-","*","/","%","&&","&","||","|","^","**","!","(",")","$",";","/*","//","*/"]


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

code = readFile("C:\\Users\\Josh\\Desktop\\Code\\Language\\program1.lang")
result = tokenize(code,"all")
        
print(result)


    
    
