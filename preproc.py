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

def preproc(code):
    code = processNewlines(code)
    code = removeComments(code)
    return code


s = "Test\nHello World\nHi//This is Josh\nThis is/* a test of*/ the preprocessor"
print(preproc(s))
