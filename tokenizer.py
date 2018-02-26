
keywords = ["let","type","impure","import","from","in","macro","do","where","for","while","if","else"]

def readFile(f):
    with open(f) as file:
        return file.read()

def tokenize(s,mode):
    
    def grabIdentifier(s):
        if s[0].isalnum():
            return str(s[0]) + str(grabIdentifier(s[1:]))
        else:
            return ""
    if mode == "identifier":
        token = grabIdentifier(s)
        if token in keywords:
            return (token, "keyword")
        else:
            return (token, "identifier")

result = tokenize("x = 5","identifier")
print(result)
    
    
