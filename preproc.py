import re
import tokenizer

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

            #grab argument list
            args = macro.split(")")[0][1:]
            macro = macro[len(args)+2:]
            args = args.split(",")
            macros.append((macro,body,args))
        else:
            lnew.append(line+";")
    for line in lnew:
        #print(macros)
        for macro in macros:
            #find match for macro
            regex = macro[0].strip()
            for arg in args:
                regex = regex.replace(arg,"[^ ;]+")
            regex = re.compile(regex)
            matchIters = [m.span() for m in re.finditer(regex,line)] #For some reason, this is not matching correctly
            for match in matchIters:
                #match is a tuple of (startIndex,endIndex)
                string = line[match[0]:match[1]+1]

                macroTokens = tokenizer.refineTokens(tokenizer.tokenize(macro[0].strip()+";","all"))
                lineTokens = tokenizer.refineTokens(tokenizer.tokenize(string,"all")) #tokenize both. Should be same length.
                
                if not len(lineTokens) == len(macroTokens):
                    print("Bad macro")
                    print(str(len(lineTokens)) + " tokens in match, but " + str(len(macroTokens)) + " tokens in macro")
                    print("Match:",string)
                    print("Match tokens:",str(lineTokens))
                    print("Macro:",macro[0].strip())
                    print("Macro tokens:",str(macroTokens))
                    break
                argvalues = {}
                for i in range(len(lineTokens)):
                    if macroTokens[i] == lineTokens[i]:
                        pass
                    elif macroTokens[i][0] in args:
                        argvalues[macroTokens[i][0]] = lineTokens[i][0] #map arguments to values
                    else:
                        print("ERROR In macro expansion!")
                newline = body
                for a,v in argvalues.items():
                    newline = newline.replace(a,v)
                line = line.replace(line[match[0]:match[1]],newline)
                print(line)
            #old way
            #line = line.replace(macro[0],macro[1])
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

