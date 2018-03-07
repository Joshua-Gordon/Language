def processNewlines(code):
    lines = code.split("\n")
    lines = list(map(lambda s: s+";",lines))
    code = ''.join(lines)
    return code

def removeComments(code):
    lines = code.split(";")
    lnew = []
    multiLine = False
    done = False
    for l in lines:
        done = False
        if multiLine and not "*/" in l:
            l = ""
        if "/*" in l:
            multiLine = True
            idx = l.find("/*")
            lnew.append(l[:idx])
            done = True
        if multiLine and "*/" in l:
            multiLine = False
            idx = l.find("*/")
            lnew.append(l[idx+2:]+";")
            done = True
        
        if "//" in l:
            idx = l.find("//")
            lnew.append(l[:idx]+";")
        elif not done:
            lnew.append(l+";")
    return ''.join(lnew)[:-1]

def expandMacros(code):
    lines = code.split(";")
    macros = []
    lnew = []
    lnew2 = []
    for line in lines:
        if line.strip()[0:5] == "macro":
            idx = line.find("=")
            macro = line[6:idx] #accounts for space after macro keyword
            body = line[idx+1:]
            macros.append((macro,body))
            #print(macro,body)
        else:
            lnew.append(line+";")
    for line in lnew:
        for macro in macros:
            line = line.replace(macro[0],macro[1])
        lnew2.append(line)
    return ''.join(lnew2)[:-1]

def preproc(code):
    code = processNewlines(code)
    #print("STAGE 1",code)
    code = removeComments(code)
    #print("STAGE 2",code)
    code = expandMacros(code)
    #print("STAGE 3",code)
    return code


s = "macro Hello=Fuck the entire\nTest\nHello World\nHi//This is Josh\nThis is/* a test of*/ the preprocessor"
print(preproc(s))
